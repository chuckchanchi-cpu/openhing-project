// ============================================================
// Google Form 標準範本（參考用）— Chuck 確認 2026-09-08
// 用途：以後所有新題目都用呢個 framework 開發，只改 addMC 內容
// 執行：揀 createForm → 執行 → 攞作答/編輯網址
// 注意：直接複製貼上，唔好修改結構（addPageBreakItem / addMC helper）
// ============================================================

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

// 新增選擇題（自動設答案、分數、回饋）— 唔好改呢個 helper
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
