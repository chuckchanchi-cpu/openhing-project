// English Grammar Practice — Unit 1: A Helping Hand (15 mins)
function createEnglishGrammarForm() {
  var form = FormApp.create('English Grammar Practice — Unit 1: A Helping Hand');
  
  // 基本設定
  form.setIsQuiz(true);
  form.setShowLinkToRespondAgain(true);
  form.setCollectEmail(false);
  
  // 發布成績設定
  form.setReleaseScore(FormApp.ReleaseScore IMMEDIATELY_AFTER_SUBMISSION);
  
  // 作答者設定
  form.setShowCorrectAnswers(true);
  form.setShowWrongAnswers(true);
  
  // 分數值設定
  form.setDefaultPointValue(0);
  
  // Section 1: Grammar 1 — so (reason and result)
  form.addPageBreakItem().setTitle('Section 1: Grammar 1 — so (原因和結果)');
  addMC(form, 'We want to help the homeless, _____ we prepare meals for them.', 'so', ['so','because','but','and'], '「so」連接原因和結果，前面加逗號');
  addMC(form, 'Chris likes helping blind people, _____ he will sell flags next month.', 'so', ['so','although','yet','or'], 'Chris 喜歡幫助盲人 → 結果：賣旗');
  addMC(form, 'Karen is good at cooking, _____ she helps her mother prepare food.', 'so', ['so','despite','however','nor'], 'Karen 擅長煮餸 → 結果：幫媽媽準備食物');
  addMC(form, 'The dog needs a home, _____ we adopt it from the SPCA.', 'so', ['so','while','since','unless'], '狗狗需要家 → 結果：從 SPCA 領養');
  addMC(form, 'I care about the environment, _____ I give away old books to recycle.', 'so', ['so','despite','nevertheless','whether'], '關心環境 → 結果：送舊書回收');
  addMC(form, 'Ben wants to raise money, _____ he plans to go on a walkathon.', 'so', ['so','although','yet','except'], '想籌錢 → 結果：參加行山活動');

  // Section 2: Grammar 2 — who / which
  form.addPageBreakItem().setTitle('Section 2: Grammar 2 — who / which（關係代詞）');
  addMC(form, 'A volunteer is a person _____ helps others without being paid.', 'who', ['who','which','what','where'], 'volunteer = person → 用 who');
  addMC(form, 'The SPCA is an animal charity _____ saves animals.', 'which', ['which','who','that','when'], 'charity = thing → 用 which');
  addMC(form, 'My aunt is a kind lady _____ can\'t see anything.', 'who', ['who','which','whose','whom'], 'lady = person → 用 who');
  addMC(form, 'This is the flag _____ Chris will sell tomorrow.', 'which', ['which','who','who','where'], 'flag = thing → 用 which');
  addMC(form, 'The children _____ are sick need our help.', 'who', ['who','which','what','where'], 'children = people → 用 who');
  addMC(form, 'A walkathon is a long walk _____ raises money for charity.', 'which', ['which','who','whom','whose'], 'walkathon = thing → 用 which');

  // Section 3: Vocabulary in Context
  form.addPageBreakItem().setTitle('Section 3: Vocabulary in Context');
  addMC(form, 'If you take an animal into your home and care for it, you _____ it.', 'adopt', ['adopt','donate','visit','sell'], 'adopt = 領養動物回家照顧');
  addMC(form, 'A person who helps others without being paid is called a _____.', 'volunteer', ['volunteer','customer','manager','buyer'], 'volunteer = 義工，免費助人');
  addMC(form, 'A long walk to collect money for charity is called a _____.', 'walkathon', ['walkathon','marathon','runathon','swimathon'], 'walkathon = 行山籌款活動');
  addMC(form, 'When you give money or things to help people, you _____.', 'donate', ['donate','collect','spend','save'], 'donate = 捐贈金錢或物品');
}

// 輔助函數：添加選擇題
function addMC(form, question, correctAnswer, options, hint) {
  var item = form.addMultipleChoiceItem();
  item.setTitle(question + '\n💡 ' + hint);
  item.setRequired(true);
  
  for (var i = 0; i < options.length; i++) {
    item.addChoice(options[i]);
  }
  
  var choices = item.getChoices();
  for (var i = 0; i < choices.length; i++) {
    if (choices[i].getValue() === correctAnswer) {
      item.correctResponse(choices[i]);
    }
  }
  
  item.setFeedbackForCorrectResponse(
    FormApp.createFeedback().setFeedbackText('✅ Correct!')
  );
  item.setFeedbackForIncorrectResponse(
    FormApp.createFeedback().setFeedbackText('❌ Wrong! The answer is: ' + correctAnswer)
  );
}
