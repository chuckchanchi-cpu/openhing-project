# Google 表單成功案例：數學練習（小數除法）

> 建立日期：2026-09-09 00:26 ｜ 狀態：✅ 成功（19 項 = 16 題 MC + 3 個 section）
> 用途：**以後所有 Google Form 練習題都用呢個 framework**，只改 `addMC` 內容。

---

## 一、成功表單連結（記錄）

**表單名稱：** 數學練習：小數除法（一）

- **作答網址：** https://docs.google.com/forms/d/e/1FAIpQLSfXZNVHVVU4H2NGNriwivdCT_5w4d-0unodRGol16OYw6XJUQ/viewform
- **編輯網址：** https://docs.google.com/forms/d/1ypY9WJl-OMk2WTMcVVoOMmoCH2RhyvQwDBRCHQyGlmI/edit

> 新表單第一次開作答網址可能見到「Google 並未認可或建立這項內容」警告 →
> 先開一次**編輯網址**（擁有人帳戶登入），之後警告消失。

---

## 二、成功 Script（完整版，直接複製貼上）

> ⚠️ **複製方法：** 用 Discord/網頁 code block 右上角嘅「**複製**」按鈕，
> **唔好用手動 mouse 揀字**（試過兩次都漏咗一半！）

```javascript
// 數學練習：小數除法（一）— 16 題 MC 版（每題附提示）
function createForm() {
  var form = FormApp.create('數學練習：小數除法（一）');
  form.setIsQuiz(true);
  form.setShowLinkToRespondAgain(true);
  form.setCollectEmail(false);

  form.addPageBreakItem().setTitle('第一部分：計算題');
  addMC(form, '6.2 ÷ 2 = ?', ['3.1','3.01','31','0.31'], '3.1', '先當整數除：62 ÷ 2 = 31，6.2 有一位小數，答案就係 3.1');
  addMC(form, '8.4 ÷ 6 = ?', ['1.4','14','0.14','1.04'], '1.4', '拆數法：6 ÷ 6 = 1，2.4 ÷ 6 = 0.4');
  addMC(form, '9.3 ÷ 3 = ?', ['3.1','3.3','31','0.31'], '3.1', '拆數法：9 ÷ 3 = 3，0.3 ÷ 3 = 0.1');
  addMC(form, '0.85 ÷ 5 = ?', ['0.17','1.7','17','0.017'], '0.17', '先當整數除：85 ÷ 5 = 17，0.85 有兩位小數');
  addMC(form, '7.5 ÷ 3 = ?', ['2.5','25','0.25','2.05'], '2.5', '拆數法：6 ÷ 3 = 2，1.5 ÷ 3 = 0.5');
  addMC(form, '6.48 ÷ 6 = ?', ['1.08','1.8','10.8','0.18'], '1.08', '拆數法：6 ÷ 6 = 1，0.48 ÷ 6 = 0.08');
  addMC(form, '48 ÷ 5 = ?', ['9.6','9.06','96','0.96'], '9.6', '唔夠除就補 0：48.0 ÷ 5');
  addMC(form, '35.7 ÷ 6 = ?', ['5.95','5.59','59.5','0.595'], '5.95', '先當整數除：357 ÷ 6 = 59.5，35.7 有一位小數');
  addMC(form, '77 ÷ 14 = ?', ['5.5','5.05','55','0.55'], '5.5', '拆數法：70 ÷ 14 = 5，7 ÷ 14 = 0.5');
  addMC(form, '50.6 ÷ 22 = ?', ['2.3','23','0.23','2.03'], '2.3', '拆數法：44 ÷ 22 = 2，6.6 ÷ 22 = 0.3');
  addMC(form, '30 ÷ 25 = ?', ['1.2','12','0.12','1.02'], '1.2', '被除數大過除數，答案大過 1。25 × 1.2 = 30');
  addMC(form, '9 ÷ 45 = ?', ['0.2','2','0.02','0.5'], '0.2', '被除數細過除數，答案細過 1');

  form.addPageBreakItem().setTitle('第二部分：分數化小數');
  addMC(form, '1/4 = ?', ['0.25','0.5','0.75','0.2'], '0.25', '分數化小數：1 ÷ 4 = 0.25。背熟：四分之一 = 0.25');
  addMC(form, '3/4 = ?', ['0.75','0.25','0.5','0.7'], '0.75', '分數化小數：3 ÷ 4 = 0.75。背熟：四分之三 = 0.75');

  form.addPageBreakItem().setTitle('第三部分：應用題');
  addMC(form, '媽媽把一條長 35.7 米的繩子平均剪成 6 段，每段長多少米？', ['5.95 米','5.59 米','59.5 米','0.595 米'], '5.95 米', '35.7 ÷ 6 = 5.95，記得答案要寫單位「米」');
  addMC(form, '一箱橙重 7.5 公斤，平均分給 3 人，每人得多少公斤？', ['2.5 公斤','25 公斤','0.25 公斤','2.05 公斤'], '2.5 公斤', '7.5 ÷ 3 = 2.5，記得答案要寫單位「公斤」');

  Logger.log('✅ 表單已建立！共 ' + form.getItems().length + ' 項');
  Logger.log('作答網址：' + form.getPublishedUrl());
  Logger.log('編輯網址：' + form.getEditUrl());
}

// 新增選擇題（MC + 提示 + 自動批改）— 唔好改呢個 helper
function addMC(form, question, choices, answer, hint) {
  var item = form.addMultipleChoiceItem();
  var choiceObjects = [];
  for (var i = 0; i < choices.length; i++) {
    choiceObjects.push(item.createChoice(choices[i], choices[i] === answer));
  }
  item.setTitle(question)
      .setChoices(choiceObjects)
      .setPoints(5)
      .setRequired(true);
  if (hint) { item.setHelpText('💡 ' + hint); }
  item.setFeedbackForCorrect(FormApp.createFeedback().setText('正確！').build());
  item.setFeedbackForIncorrect(FormApp.createFeedback().setText('錯誤！正確答案是：' + answer).build());
}
```

---

## 三、開發新表單步驟（照抄）

1. 改 `FormApp.create('表單名稱')` 個名
2. 每個 section：`form.addPageBreakItem().setTitle('部分名稱');`
3. 每題一行：`addMC(form, '題目', ['A','B','C','D'], '正確答案', '提示文字');`
4. 提示唔想要可以留空：`addMC(form, '題目', [...], '答案', '');`
5. **Ctrl+S** → 揀 `createForm` → 執行
6. 執行記錄攞作答/編輯網址

---

## 四、正確 API 名稱（唔好再用錯）

| ❌ 錯 | ✅ 啱 | 備註 |
|---|---|---|
| `form.addPageBreak(...)` | `form.addPageBreakItem().setTitle(...)` | 分頁/section |
| `form.addShortAnswerItem(...)` | `form.addTextItem(...)` | 短答題（我哋用 MC 所以唔使） |
| `item.newChoice(...)` | `item.createChoice(value, isCorrect)` | 加選項 |
| `item.addChoice(...)` | `item.createChoice(value, isCorrect)` | 加選項 |
| `FormApp.createChoice(...)` | `item.createChoice(value, isCorrect)` | createChoice 係 item 嘅 method |
| `FormApp.getUi()` | ❌ 刪走 | 獨立 script 用唔到 |
| feedback 冇 `.build()` | `FormApp.createFeedback().setText(...).build()` | 一定要 build |

---

## 五、執行記錄範例（成功）

```
✅ 表單已建立！共 19 項
作答網址：https://docs.google.com/forms/d/e/1FAIpQLSfXZNVHVVU4H2NGNriwivdCT_5w4d-0unodRGol16OYw6XJUQ/viewform
編輯網址：https://docs.google.com/forms/d/1ypY9WJl-OMk2WTMcVVoOMmoCH2RhyvQwDBRCHQyGlmI/edit
```

19 項 = 16 題 MC + 3 個 section 分隔 ✅
