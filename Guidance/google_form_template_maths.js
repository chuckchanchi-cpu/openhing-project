// ============================================================
// Google Form 範本（數學版）— MC + 每題提示 + 自動批改
// 日期：2026-09-09 ｜ 內容：小數除法（一）16 題
// 用法：貼上 → Ctrl+S → 揀 createForm → 執行
// 注意：API 正確名稱 —— item.createChoice()（唔係 newChoice/addChoice/FormApp.createChoice）
//       item.setHelpText() = 題目下面嘅提示文字
//       獨立 script 唔可以用 FormApp.getUi()
// ============================================================

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

// 新增選擇題（MC + 提示 + 自動批改）
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
