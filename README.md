# MCDR-Hat

## 此專案已停止維護 
--------------  
#### 因為py json無法解析minecraft nbt的整型陣列(number:[I;1,2,3,4,5]等形式  
#### 在操作物品時NBT中的attribute modifier會被MinecraftDataAPI丟棄導致物品資料遺失
#### 若服務器有在使用carpet模組 建議考慮另外一個專案中用scarpet實現的`/hat`
https://github.com/B-2U/Scarpet-scripts
---------------------
## 前置 / Requirement
- [MinecraftDataAPI](https://github.com/MCDReforged/MinecraftDataAPI)
## 指令 / Command
- `!!hat` 將手上跟頭上的物品交換位置 / Swap the item on your hand and head
