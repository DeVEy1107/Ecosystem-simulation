
# 人工智慧導論期末報告 

## 主題

這一個程式碼的主題是生態系統模擬，模擬生物在環境中覓食、繁殖的行為。


## 方法

### ``地形生成``

模擬生態除了生物以外，另一個重要的要素是環境，環境的部份其中包含了地形及糧食生成。首先是地形的部份，需要得到的一個具有自然紋理和隨機性的圖形的二維陣列，而在這邊使用的方法是透過"Perlin noise"(柏林噪聲)一種隨機噪聲生成演算法來生成。

下面是視覺化柏林噪聲產生的二維陣列

![](images/readme/perlinNoise2d.jpeg)

而這一個是立體空間中的柏林噪聲生成的圖形

![](images/readme/perlinNoise3d.png)

在實作的部份，我使用python提供的套件"perlin_noise"來實現柏林噪聲的功能。
我在程式碼中得到的一組包含[-1.0, 1.0]的二維陣列資料，並將其歸一化至[0.0, 1.0]。

接著原本得到的二維陣列資料中每一個索引值以[0.0, 0.3), [0.3, 0.35), [0.35, 1.0]三個部份來做區分，分別得到水地、沙土及草地的地貌。

為了避免地形樣貌過多而導致內容過於複雜，在這邊只使用三種地形樣貌。

![](images/readme/terrainExample.png)

以下是地形對生物造成的影響：
- 水地：生物移動速度降低

- 其餘對生物無影響

### ``糧食``

- 牧草

    在地圖上任何位置會隨時間隨機生長一定數量的牧草給綿羊吃

  ![](images/readme/grass.png)

### ``生物``

在這邊直接介紹實作的部分。

#### - 生物參數

首先，定義的生物類別中的重要參數如下：

- hungerLevel: 生物的飢餓值，會隨著時間而降低，低於0時生物死亡 
- hungerSpeed: 飢餓值隨時間改變的變化量
- matingDesireLevel: 繁殖衝動水平的量值，隨時間增加，達到閾值時可以進行繁殖
- matingDesireSpeed: matingDesireLevel的增長隨時間增加的變化量
- matingDesireThreshold: matingDesireLevel可以進行繁殖的閾值
- speed: 生物的移動速度
- detectionRange: 偵測週邊生物的範圍
- interactiveRange: 開始進行覓食、繁殖的互動範圍
- towarfFoodSpeed: 朝向食物的移動速度


#### - 生物基礎行為方法

定義的生物基本行為有以下三種：

```mermaid
flowchart

b1(隨機移動)
b2(覓食)
b3(繁殖)
```

- 隨機移動: 隨時間移動及改變方向
- 覓食: 偵測到食物則向食物的方向跑去
- 繁殖: 符合繁殖條件時進行繁殖，誕生新生命

#### - 生物種類
- **綿羊**
  
  以牧草為食的動物，其可執行的行為多了"逃跑"，偵測到狩獵者載周圍時則開始逃離狩獵者

  ```mermaid
  flowchart

  b1(隨機移動)
  b2(覓食)
  b3(繁殖)
  b4(逃跑)
  ```

  ![](images/readme/sheep.png)

  - 綿羊的行為決策

  ```mermaid
  flowchart TD
  t1(偵測範圍) 
  cond1(有掠食者在周圍?)

  t1 ==> cond1
  cond1 ==有==> r1(逃跑)
  cond1 ==沒有==> cond2(有同類在周圍?)

  cond2 ==有==> cond3(兩者皆 matingDesireLevel >= matingDesireThreshold?)
  cond3 ==有==> r2(繁殖)
  cond3 ==沒有==> cond4(有食物在周圍?)

  cond4 ==有==> r3(覓食)
  cond4 ==沒有==> r4(隨意行走)

  cond2 ==沒有==> cond4
  ```

- **狼**

  以猴子為狩獵的對象

  ```mermaid
  flowchart

  b1(隨機移動)
  b2(覓食)
  b3(繁殖)
  ```

  ![](images/readme/wolf.png)


- 狼的行為決策
  ```mermaid
  flowchart TD
  t1(偵測範圍) 

  t1 ==> cond2(有同類在周圍?)

  cond2 ==有==> cond3(兩者皆 matingDesireLeve >= matingDesireThreshold?)
  cond3 ==有==> r2(繁殖)
  cond3 ==沒有==> cond4(有猴子在周圍?)

  cond4 ==有==> r3(狩獵)
  cond4 ==沒有==> r4(隨意行走)

  cond2 ==沒有==> cond4
  ```

## 環境建立與執行方式

使用python版本為3.8.10

- 需安裝的套件:
  - numpy
  - pygame
  - perlin_noise

安裝指令:
```
pip install -r requirements.txt
```

執行src資料中的main.py

## 操作方式
執行遊戲後可按下P鍵暫停遊戲來進行布局。

操作按鍵細節:
- R按鍵: 重置遊戲
- P按鍵: 暫停遊戲
- Q按鍵: 離開遊戲
- 左鍵: 放置狼
- 右鍵: 放置猴子
- Tab按鍵: 顯示當前生物及糧食數量
- S按鍵: 顯示生物數值、偵測及互動範圍
- 上、下、左、右按鍵: 移動視窗畫面


## 參考資料

> [Coding Adventure: Simulating an Ecosystem](https://www.youtube.com/watch?v=r_It_X7v-1E&t=160s)

> [Making maps with noise functions](https://www.redblobgames.com/maps/terrain-from-noise/)

