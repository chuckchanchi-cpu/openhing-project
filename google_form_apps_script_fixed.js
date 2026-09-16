function createForm() {
  const form = FormApp.getActiveForm();
  
  // 清空現有題目
  const items = form.getItems();
  for (let i = items.length - 1; i >= 0; i--) {
    form.deleteItem(items[i]);
  }
  
  // Section 1: 中文填充
  const section1 = form.addSection('中文填充');
  const chineseVocab = [
    ['他________地來到這塊麥田邊，想揀到最大的一棵麥穗。', '慕名'],
    ['看到顆粒飽滿的麥穗，有人想摘又________，總覺得後面還有更大的。', '不忿'],
    ['蘇格拉底________地對學生說：「人生就是一次無法重複的選擇。」', '語重心長'],
    ['陽光灑在麥田上，看起來________一片，非常美麗。', '金燦燦'],
    ['如果________了這個機會，以後可能就再也沒有第二次了。', '錯過'],
    ['經過反覆思考，他才________明白到把握眼前最重要。', '恍然大悟'],
    ['這是我們________一次嘗試嘅機會，一定要好好珍惜。', '唯一'],
    ['每棵麥穗都________的，看起來非常飽滿。', '沉甸甸'],
    ['雖然前面還有更遠嘅目標，但他知道這裡就是旅程嘅________。', '盡頭'],
    ['只要遵守學校的________，每個人都能安全通過走廊。', '規矩']
  ];
  
  for (const [q, a] of chineseVocab) {
    const item = section1.addShortAnswerItem(q);
    item.setRequired(true);
    setFeedback(item, a, a);
  }
  
  // Section 2: 中文語法
  const section2 = form.addSection('中文語法');
  const chineseGrammar = [
    ['「他因為热爱閱讀，所以每天都會去圖書館借書。」連接詞是？', '因為...所以'],
    ['「她不僅會彈鋼琴，而且還擅長畫畫。」連接詞是？', '不僅...而且'],
    ['「即使下雨，我們也會按时到校上課。」連接詞是？', '即使...也'],
    ['「她的笑容像陽光照進我的心裡。」修辭手法？', '明喻/比喻'],
    ['「時間是流水，一去不再回。」修辭手法？', '暗喻/比喻']
  ];
  
  for (const [q, a] of chineseGrammar) {
    const item = section2.addShortAnswerItem(q);
    item.setRequired(true);
    setFeedback(item, a, a);
  }
  
  // Section 3: 英文語法
  const section3 = form.addSection('英文語法');
  const englishGrammar = [
    ['I want to help the homeless. I prepare meals for them sometimes. (用 so 結合)', 'I want to help the homeless, so I prepare meals for them sometimes.'],
    ['She wants to raise money. She plans to go on a walkathon. (用 so 結合)', 'She wants to raise money, so she plans to go on a walkathon.'],
    ['He cares about the environment. He gives away old books to recycle. (用 so 結合)', 'He cares about the environment, so he gives away old books to recycle.'],
    ['The SPCA is an animal charity. It protects and saves animals. (用 which 結合)', 'The SPCA is an animal charity which protects and saves animals.'],
    ['Anna is a volunteer. She helps elderly people in need. (用 who 結合)', 'Anna is a volunteer who helps elderly people in need.'],
    ['The Doggy Inn is a special hotel. It lets guests take dogs for walks. (用 which 結合)', 'The Doggy Inn is a special hotel which lets guests take dogs for walks.']
  ];
  
  for (const [q, a] of englishGrammar) {
    const item = section3.addShortAnswerItem(q);
    item.setRequired(true);
    setFeedback(item, a, a);
  }
  
  // Section 4: 常識生物分類
  const section4 = form.addSection('常識生物分類');
  const generalStudy = [
    ['蛙、蠑螈屬於哪一類？', '兩棲類'],
    ['蛇、海龜屬於哪一類？', '爬行類'],
    ['蝙蝠、海豚屬於哪一類？', '哺乳類'],
    ['蜜蜂屬於哪一類（無脊椎動物）？', '昆蟲類'],
    ['苔蘚類和蕨類以什麼繁殖？', '孢子'],
    ['有花植物與無花植物的主要分別是什麼？', '有花植物會開花結果；無花植物永不開花']
  ];
  
  for (const [q, a] of generalStudy) {
    const item = section4.addShortAnswerItem(q);
    item.setRequired(true);
    setFeedback(item, a, a);
  }
  
  FormApp.getUi().alert('✅ 表單已建立完成！共 ' + form.getItems().length + ' 題');
}

function setFeedback(item, correct, incorrect) {
  item.createResponseValidator(
    FormApp.createShortAnswerResponseValidator().setValidationFunction(
      function(answer) {
        return answer.getValue().trim() === correct.trim();
      }
    )
  );
  item.setFeedbackForCorrectResponse(
    FormApp.createFeedback().setFeedbackText('✅ 正確！')
  );
  item.setFeedbackForIncorrectResponse(
    FormApp.createFeedback().setFeedbackText('❌ 錯誤！正確答案是：' + correct)
  );
}
