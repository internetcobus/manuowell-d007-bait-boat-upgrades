// Battery gauge for the Manuowell D007 (Waveshare ESP32-C3-Zero).
//
// Reads the pack through a 330k / 10k divider (+100 nF) on GPIO3 and shows the
// charge on the hull's 4 LEDs as a bar: red = the first segment, then the 3
// blues. Each LED runs from 5 V through 330 R, switched by a BC547 (10k base),
// so a GPIO driven HIGH turns its LED ON. (The 330 R sits on the cathode side;
// the LED strip's long legs share 5 V.)
//
//   bar         per cell (filtered)      6S pack
//   4 LEDs      >= 3.90 V                >= 23.4 V
//   3 LEDs      >= 3.70 V                >= 22.2 V
//   2 LEDs      >= 3.50 V                >= 21.0 V
//   red only    >= 3.30 V                >= 19.8 V   (= the Pixhawk's RTL level)
//   red flash   <  3.30 V                <  19.8 V   (RTL has triggered: come home)
//
// The cell count is detected at power-up (2S stock pack, 4S, or 6S). Under
// throttle the pack sags, so the reading is smoothed (about 10 s) and a level
// only changes once the voltage is 0.05 V/cell past its threshold: e.g. the
// red starts flashing at 3.25 V/cell (19.5 V on 6S), just after the RTL.
//
// Serial (115200, USB):
//   every 2 s:  pack volts, per-cell, cells, level, raw ADC mV, divider ratio
//   cal 24.46   set the divider ratio from a multimeter reading of the pack
//               (saved in flash, survives power-off)
//   cal reset   back to the nominal 34.0
//
// The ESP32-C3's USB serial DISCARDS output when no terminal has the port open
// (camping fan lesson): keep the monitor open while testing.

#include <Arduino.h>
#include <Preferences.h>

// --- pins (see the layout picture in docs/04) --------------------------------
static const int PIN_VSENSE = 3;   // ADC1_CH3, the divider node

// LED positions along the hull row, P1 = the one next to the GPS status LED.
static const int PIN_LED[4] = {4, 5, 6, 7};   // P1, P2, P3, P4 (driver board A6, D6, G6, J6)

// Which end the red LED is fitted at. true: red in P1 (next to the GPS LED).
static const bool RED_AT_GPS_END = true;

// PWM brightness 0-255 per LED. Through 330 R from 5 V the red runs about
// 9 mA and the blues about 6 mA, so the red is turned down to look even.
static const uint8_t BRIGHT_RED  = 150;
static const uint8_t BRIGHT_BLUE = 255;

// --- battery ------------------------------------------------------------------
static const float DIV_NOMINAL = (330.0f + 10.0f) / 10.0f;   // 34.0 (was 220k / 23.0 until 2026-10-18)
static const float LEVEL_V[4]  = {3.30f, 3.50f, 3.70f, 3.90f};  // per cell
static const float HYST_V      = 0.05f;   // per cell
static const float SMOOTH_TAU_S = 10.0f;
static const float NO_BATTERY_V = 5.0f;   // below this: USB only, no pack

static Preferences prefs;
static float div_ratio = DIV_NOMINAL;
static float adc_mv = 0.0f;       // last raw reading, kept for calibration
static float v_smooth = 0.0f;
static int cells = 0;             // 0 = not detected yet
static int level = -1;            // 0..4 segments; 0 = flash red

static float read_pack_volts() {
    uint32_t acc = 0;
    for (int i = 0; i < 16; i++) acc += analogReadMilliVolts(PIN_VSENSE);
    adc_mv = acc / 16.0f;
    return adc_mv * 0.001f * div_ratio;
}

static int detect_cells(float v) {
    if (v < NO_BATTERY_V) return 0;
    if (v < 9.0f)  return 2;      // stock 7.4 V pack (8.4 V full)
    if (v < 17.5f) return 4;      // 16.8 V full
    return 6;                     // 25.2 V full
}

// Segment n (1..4) -> LED position index 0..3.
static int seg_to_pos(int seg) {
    return RED_AT_GPS_END ? seg - 1 : 4 - seg;
}

static void led_set(int pos, bool on) {
    bool is_red = (pos == seg_to_pos(1));
    ledcWrite(pos, on ? (is_red ? BRIGHT_RED : BRIGHT_BLUE) : 0);
}

static void show_bar(int segments) {
    for (int s = 1; s <= 4; s++) led_set(seg_to_pos(s), s <= segments);
}

// New level from the per-cell voltage, with hysteresis around the current one.
static int next_level(float vc, int current) {
    int raw = 0;
    for (int i = 0; i < 4; i++) if (vc >= LEVEL_V[i]) raw = i + 1;
    if (current < 0) return raw;
    if (raw > current) {          // rising: must clear the threshold by HYST_V
        int up = current;
        while (up < 4 && vc >= LEVEL_V[up] + HYST_V) up++;
        return up;
    }
    if (raw < current) {          // falling: must drop HYST_V below it
        int down = current;
        while (down > 0 && vc < LEVEL_V[down - 1] - HYST_V) down--;
        return down;
    }
    return current;
}

static void handle_serial() {
    static String line;
    while (Serial.available()) {
        char c = Serial.read();
        if (c != '\n' && c != '\r') { line += c; continue; }
        line.trim();
        if (line == "cal reset") {
            div_ratio = DIV_NOMINAL;
            prefs.putFloat("div", div_ratio);
            Serial.printf("divider ratio reset to %.4f\n", div_ratio);
        } else if (line.startsWith("cal ")) {
            float meter = line.substring(4).toFloat();
            if (meter > 1.0f && adc_mv > 50.0f) {
                div_ratio = meter / (adc_mv * 0.001f);
                prefs.putFloat("div", div_ratio);
                v_smooth = meter;
                Serial.printf("calibrated: %.2f V at %.0f mV -> ratio %.4f (saved)\n",
                              meter, adc_mv, div_ratio);
            } else {
                Serial.println("cal: need a pack connected and a reading like 'cal 24.46'");
            }
        } else if (line.length()) {
            Serial.println("commands: cal <meter volts> | cal reset");
        }
        line = "";
    }
}

void setup() {
    Serial.begin(115200);
    prefs.begin("gauge", false);
    div_ratio = prefs.getFloat("div", DIV_NOMINAL);

    analogSetPinAttenuation(PIN_VSENSE, ADC_11db);   // ~0.74 V on the pin at 25.2 V

    for (int i = 0; i < 4; i++) {
        ledcSetup(i, 1000, 8);
        ledcAttachPin(PIN_LED[i], i);
        ledcWrite(i, 0);
    }

    // Power-up sweep: every LED on in turn, so a dead one is obvious.
    for (int s = 1; s <= 4; s++) { show_bar(s); delay(200); }
    delay(300);
    show_bar(0);

    v_smooth = read_pack_volts();
    cells = detect_cells(v_smooth);
}

void loop() {
    static uint32_t last_sample = 0, last_report = 0;
    uint32_t now = millis();
    handle_serial();

    if (now - last_sample >= 100) {
        float dt = (now - last_sample) * 0.001f;
        last_sample = now;
        float v = read_pack_volts();
        v_smooth += (v - v_smooth) * (dt / (SMOOTH_TAU_S + dt));
        if (v < NO_BATTERY_V) {
            cells = 0;                           // pack unplugged (on USB): re-detect the next one
        } else if (cells == 0) {                 // pack connected after USB power-up
            v_smooth = v;
            cells = detect_cells(v);
            level = -1;
        }
    }

    if (cells == 0) {
        // No pack (USB only): slow blink of the red, so the board shows it's alive.
        show_bar(0);
        led_set(seg_to_pos(1), (now / 1000) % 2 == 0);
    } else {
        level = next_level(v_smooth / cells, level);
        if (level == 0) {
            show_bar(0);
            led_set(seg_to_pos(1), (now / 250) % 2 == 0);   // fast flash: below RTL level
        } else {
            show_bar(level);
        }
    }

    if (now - last_report >= 2000) {
        last_report = now;
        Serial.printf("pack %.2f V  cell %.3f V  %dS  level %d  adc %.0f mV  ratio %.4f\n",
                      v_smooth, cells ? v_smooth / cells : 0.0f, cells, level, adc_mv, div_ratio);
    }
}
