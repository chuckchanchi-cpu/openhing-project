# Google 表單：批量建立題目與批改指引

> 用途：用 Apps Script 一次過建立測驗模式嘅 Google 表單（自動批改、自動計分），
> 亦支援用 CSV 批量入題。建立日期：2026-09-08（車程高效訓練 40 題版）。

---

## 一、建立新表單（Apps Script 方法）

### Step 1：開啟 Apps Script
1. 打開 <https://script.google.com>
2. 撳「**+ 新增專案**」
3. 刪走編輯器入面所有預設內容

### Step 2：貼上程式碼
將下方完整程式碼貼入編輯器（**直接貼，唔好修改任何嘢**）。

```javascript
// 30 分鐘車程高效訓練 — 40 題
function createForm() {
  var form = FormApp.create('30 分鐘車程高效訓練');
  form.setIsQuiz(true);
  form.setShowLinkToRespondAgain(true);
  form.setCollectEmail(false);

  // 第一部分：中文填充
  form.addPageBreakItem().setTitle('第一部分：中文填充');
  addMC(form, '他＿＿＿＿了一會，才決定摘下那棵麥穗。', ['躊躇','捨棄','錯過','漫長'], '躊躇');
  addMC(form, '聽完老師的解釋，他＿＿＿＿。', ['恍然大悟','語重心長','不約而同','慕名'], '恍然大悟');
  addMC(form, '老師＿＿＿＿地勸我們要珍惜時間。', ['語重心長','金燦燦','沉甸甸','漫長'], '語重心長');
  addMC(form, '大家＿＿＿＿地鼓起掌來。', ['不約而同','恍然大悟','躊躇','捨棄'], '不約而同');
  addMC(form, '切勿錯失＿＿＿＿。', ['良機','盡頭','規矩','麥穗'], '良機');
  addMC(form, '許多遊客＿＿＿＿而來，品嘗這家老店的點心。', ['慕名','躊躇','捨棄','唯一'], '慕名');
  addMC(form, '夕陽把麥田照得＿＿＿＿的。', ['金燦燦','沉甸甸','漫長','規矩'], '金燦燦');
  addMC(form, '他捧着＿＿＿＿的獎杯，十分興奮。', ['沉甸甸','金燦燦','唯一','盡頭'], '沉甸甸');
  addMC(form, '這是他＿＿＿＿的機會，一定要好好珍惜。', ['唯一','良機','漫長','慕名'], '唯一');
  addMC(form, '我們要遵守學校的＿＿＿＿。', ['規矩','盡頭','良機','麥穗'], '規矩');

  // 第二部分：中文文法
  form.addPageBreakItem().setTitle('第二部分：中文文法');
  addMC(form, '「＿＿＿得到最大的麥穗固然理想，＿＿＿後面可能有更大的。」應填甚麼關聯詞？', ['雖然……但是……','因為……所以……','不但……而且……','如果……就……'], '雖然……但是……');
  addMC(form, '課文中「麥穗」借喻甚麼？', ['機會','收成','糧食','種子'], '機會');
  addMC(form, '「雨後的彩虹宛如一座七彩的橋。」運用了甚麼修辭手法？', ['明喻','暗喻','借喻','擬人'], '明喻');
  addMC(form, '「他放棄了這棵麥穗，＿＿＿想往前找找看。」應填甚麼關聯詞？', ['因為','但是','雖然','如果'], '因為');
  addMC(form, '下列哪一句是「暗喻」？', ['「時間就是金錢。」','「月亮像一個玉盤。」','「他跑得比兔子還快。」','「春風又綠江南岸。」'], '「時間就是金錢。」');
  addMC(form, '「她＿＿＿會彈鋼琴，＿＿＿還擅長畫畫。」應填甚麼關聯詞？', ['不但……而且……','雖然……但是……','因為……所以……','與其……不如……'], '不但……而且……');
  addMC(form, '「＿＿＿下雨，我們＿＿＿會按時到校上課。」應填甚麼關聯詞？', ['即使……也……','因為……所以……','不但……而且……','如果……就……'], '即使……也……');
  addMC(form, '他因為熱愛閱讀，＿＿＿每天都去圖書館借書。應填甚麼關聯詞？', ['所以','但是','雖然','如果'], '所以');
  addMC(form, '「宛如」與下列哪個詞意思最接近？', ['好像','捨棄','躊躇','唯一'], '好像');
  addMC(form, '下列哪一組是近義詞？', ['躊躇和猶豫','麥穗和機會','規矩和良機','捨棄和唯一'], '躊躇和猶豫');

  // 第三部分：英文文法
  form.addPageBreakItem().setTitle('Part 3: English Grammar');
  addMC(form, 'She helps people ____ have no home.', ['who','which','so','where'], 'who');
  addMC(form, 'The SPCA is an animal charity ____ helps and saves animals.', ['which','who','so','but'], 'which');
  addMC(form, 'We have adopted a pet from the SPCA recently, ____ I hope you can help the SPCA.', ['so','because','but','where'], 'so');
  addMC(form, 'We can visit hospitals and play games with children ____ are sick.', ['who','which','so','where'], 'who');
  addMC(form, 'I will go on a walkathon soon, ____ I can collect money to help blind people.', ['so','but','where','when'], 'so');
  addMC(form, 'I want to help the homeless, ____ I help prepare meals for them.', ['so','who','which','but'], 'so');
  addMC(form, 'We can support a food charity ____ prepares food for people in need.', ['which','who','so','but'], 'which');
  addMC(form, 'We can give clothes and toys to boys and girls ____ need them.', ['who','which','so','where'], 'who');
  addMC(form, 'Chris ____ flags on the street to raise money.', ['sells','buys','gives','adopts'], 'sells');
  addMC(form, 'Ben will ____ to collect money for charity.', ['go on a walkathon','adopt a pet','sell flags','visit an elderly home'], 'go on a walkathon');

  // 第四部分：常識
  form.addPageBreakItem().setTitle('第四部分：常識');
  addMC(form, '蛙的皮膚濕潤、沒有鱗片，成長後用肺和皮膚呼吸。牠屬於哪一類？', ['兩棲類','爬行類','魚類','哺乳類'], '兩棲類');
  addMC(form, '蝙蝠有翅膀會飛，但有毛髮、用母乳餵養幼兒。牠屬於哪一類？', ['哺乳類','鳥類','爬行類','兩棲類'], '哺乳類');
  addMC(form, '海龜有殼、皮膚乾燥、有鱗片、用肺呼吸。牠屬於哪一類？', ['爬行類','魚類','哺乳類','兩棲類'], '爬行類');
  addMC(form, '判斷：魚類用肺呼吸。', ['正確','錯誤'], '錯誤');
  addMC(form, '蕨類以甚麼繁殖？', ['孢子','種子','球果','花朵'], '孢子');
  addMC(form, '蜜蜂有三對腳、身體分頭胸腹三部分、有一對觸角。牠屬於哪一類？', ['昆蟲類','鳥類','兩棲類','哺乳類'], '昆蟲類');
  addMC(form, '蠑螈皮膚濕潤、無鱗片、成長後用肺和皮膚呼吸。牠屬於哪一類？', ['兩棲類','爬行類','魚類','哺乳類'], '兩棲類');
  addMC(form, '判斷：所有爬行類都有四隻腳。', ['正確','錯誤'], '錯誤');
  addMC(form, '課文中提到的兩種無花植物是甚麼？', ['苔蘚類和蕨類','睡蓮和鳳凰木','海藻和睡蓮','松樹和鳳凰木'], '苔蘚類和蕨類');
  addMC(form, '松樹的種子生在甚麼地方？', ['球果內','花朵裏','葉子上','根部'], '球果內');

  Logger.log('✅ 表單已建立！共 ' + form.getItems().length + ' 項');
  Logger.log('作答網址：' + form.getPublishedUrl());
  Logger.log('編輯網址：' + form.getEditUrl());
}

// 新增選擇題（自動設答案、分數、回饋）
function addMC(form, question, choices, answer) {
  var item = form.addMultipleChoiceItem();
  var choiceObjects = [];
  for (var i = 0; i < choices.length; i++) {
    choiceObjects.push(item.createChoice(choices[i], choices[i] === answer));
  }
  item.setTitle(question)
      .setChoices(choiceObjects)
      .setPoints(5)
      .setRequired(true);
  item.setFeedbackForCorrect(FormApp.createFeedback().setText('正確！').build());
  item.setFeedbackForIncorrect(FormApp.createFeedback().setText('錯誤！正確答案是：' + answer).build());
}
```

### Step 3：執行
1. 撳 **Ctrl+S** 儲存
2. 編輯器頂部揀函數 **`createForm`**
3. 撳「**執行**」▶️
4. 第一次會彈授權視窗 → 揀 Google 帳戶 → 「**進階**」→「**前往 車程訓練（不安全）**」→「**允許**」
5. 撳下方「**執行記錄**」→ 見到「✅ 表單已建立！」同**作答網址 / 編輯網址**

---

## 二、用 CSV 批量入題（可選）

將 CSV 上傳去 Google Drive（檔名 `questions.csv`），再執行 `createFormFromCSV`。

```javascript
// 從 Drive 的 questions.csv 批量建立表單
// CSV 格式：問題, 選項A, 選項B, 選項C, 選項D, 正確答案
// 開新一節嘅行：SECTION, 節名稱
function createFormFromCSV() {
  var files = DriveApp.getFilesByName('questions.csv');
  if (!files.hasNext()) {
    Logger.log('❌ 找不到 questions.csv，請先上傳到 Google Drive');
    return;
  }
  var csv = files.next().getBlob().getDataAsString('UTF-8');
  var rows = Utilities.parseCsv(csv);
  var form = FormApp.create('30 分鐘車程高效訓練');
  form.setIsQuiz(true);
  form.setShowLinkToRespondAgain(true);
  for (var i = 0; i < rows.length; i++) {
    var r = rows[i];
    if (r[0] === 'SECTION') { form.addPageBreakItem().setTitle(r[1]); continue; }
    addMC(form, r[0], [r[1], r[2], r[3], r[4]], r[5]);
  }
  Logger.log('✅ 表單已建立！作答網址：' + form.getPublishedUrl());
}
```

**CSV 範例格式：**
```
SECTION,第一部分：中文填充
他＿＿＿＿了一會，才決定摘下那棵麥穗。,躊躇,捨棄,錯過,漫長,躊躇
聽完老師的解釋，他＿＿＿＿。,恍然大悟,語重心長,不約而同,慕名,恍然大悟
SECTION,第二部分：中文文法
課文中「麥穗」借喻甚麼？,機會,收成,糧食,種子,機會
```

> 儲存 CSV 用**記事本**，編碼揀 **UTF-8**，先上傳到 Google Drive。

---

## 三、如何睇批改結果（自動批改）

1. 打開**編輯網址** → 表單頂部撳「**回覆**」分頁
2. 撳「**摘要**」→ 每題統計（邊個選項幾多人揀、啱錯比例）
3. 撳「**個別**」→ 逐份睇答案：✅ 綠色 = 啱、❌ 紅色 = 錯（自動顯示正確答案）、右上角總分
4. 撳綠色**試算表圖示（📊）**→「建立新的試算表」→ 之後所有作答自動入表，可以追蹤進步

**設定確認：**
- 右上「**設定**」（齒輪）→「**測驗**」分頁
- 「回應者可以查看的內容」揀「**提交後立即查看**」→ 提交後即時顯示分數

---

## 四、常見錯誤（Troubleshooting）

| 錯誤訊息 | 原因 | 解決方法 |
|---|---|---|
| `FormApp.getActive is not a function` | 冇 `getActive()` 呢個方法 | 獨立 script 用 `FormApp.create()`；綁定表單先用 `getActiveForm()` |
| `form.addSection is not a function` | 冇 `addSection()` | 用 `form.addPageBreakItem().setTitle('節名稱')` |
| `form.addPageBreak is not a function` | 方法名漏咗 `Item` | 用 `form.addPageBreakItem().setTitle('節名稱')` |
| `setFeedbackForCorrect` 參數唔啱 | 要傳完成嘅 feedback 物件 | 結尾加 `.build()`：`FormApp.createFeedback().setText('...').build()` |
| 開啟作答網址見到「Google 並未認可或建立這項內容」 | 表單由 Apps Script 建立，Google 未確認 | 用**編輯網址**打開一次（登入擁有人帳戶），之後警告消失；無痕視窗測試可正常作答 |

---

## 五、現有表單記錄（2026-09-08）

**40 題版（現用）：**
- 作答：https://docs.google.com/forms/d/e/1FAIpQLSfa58z_6o367Xqh_rYNV9055mNhNDWeY17HwYrpnFVnZEbZvA/viewform
- 編輯：https://docs.google.com/forms/d/1azCWUft4hCs7FNIvqPMLb3aqHIsSaQF4Lv1pPcpdkHc/edit

**舊 20 題版（可刪除）：**
- 編輯：https://docs.google.com/forms/d/1XbsPRFLapAVVW2qyiJ6yFZmvZbiWYANOfU9XvhAjy7U/edit
