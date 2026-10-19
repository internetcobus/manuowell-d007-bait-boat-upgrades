--[[
   batt_volt_pct.lua: battery % from VOLTAGE only, for the Manuowell D007.

   Why: the PM06's current reading carries several amps of interference from
   the 1 W SiK radio (docs/03), so ArduPilot's normal mAh-based % is useless.
   ArduPilot's own BattEstimate.lua only updates while DISARMED (this boat is
   always armed, ARMING_REQUIRE 0) and corrects for sag using the current.

   This script: every second, smooth the raw pack voltage (about 30 s), turn
   volts per cell into % on a Li-ion curve (Samsung 30Q cells) that matches the
   hull gauge's LED levels, and every 5 s write it into battery 1 with
   reset_remaining(). Armed or not. The current reading is never used.

   Needs: SCR_ENABLE 1, SCR_HEAP_SIZE 24576 (44032 left only ~12 KB free and
   broke MAVFTP), BATT_CAPACITY > 10 (6000) or no % is reported at all.
   Failsafes are untouched: voltage only, mAh triggers 0. The mAh-used figure
   becomes meaningless (reset_remaining rewrites it).

   Install: copy to APM/scripts/ on the Pixhawk's SD card, power-cycle.
--]]

local BATT = 0            -- battery instance (0 = BATT_)
local TAU_S = 30          -- smoothing time constant, seconds
local PUSH_EVERY = 5      -- write the % every 5 updates (s)
local NO_PACK_V = 5.0     -- below this: no pack, do nothing
local CELLS = 6           -- fixed: the failsafe voltages assume 6S too. (Auto-detect
                          -- would call a nearly flat 6S at 17 V a full 4S.)

-- volts per cell -> %, Li-ion (30Q), lined up with the gauge LEDs
local CURVE = {
   {3.10,   0},  -- BATT_CRT_VOLT 18.6 V on 6S
   {3.30,  10},  -- red only, BATT_LOW_VOLT 19.8 V (RTL)
   {3.50,  25},  -- 2 LEDs
   {3.70,  45},  -- 3 LEDs
   {3.90,  70},  -- 4 LEDs
   {4.20, 100},  -- full
}

local v_smooth = nil
local count = 0

local function pct_from_cell(vc)
   if vc <= CURVE[1][1] then return CURVE[1][2] end
   for i = 2, #CURVE do
      local v1, p1 = CURVE[i - 1][1], CURVE[i - 1][2]
      local v2, p2 = CURVE[i][1], CURVE[i][2]
      if vc <= v2 then
         return p1 + (p2 - p1) * (vc - v1) / (v2 - v1)
      end
   end
   return 100
end

local function update()
   local v = battery:voltage(BATT)
   if v == nil or v < NO_PACK_V then
      v_smooth = nil
      return update, 1000
   end
   if v_smooth == nil then
      v_smooth = v
      gcs:send_text(6, string.format("Batt%%: pack at %.2f V", v))
   else
      v_smooth = v_smooth + (v - v_smooth) * (1.0 / (TAU_S + 1.0))
   end
   count = count + 1
   if count >= PUSH_EVERY then
      count = 0
      local pct = pct_from_cell(v_smooth / CELLS)
      battery:reset_remaining(BATT, pct)
   end
   return update, 1000
end

gcs:send_text(6, "Batt%: voltage-based battery % loaded")
return update, 1000
