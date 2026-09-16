// 常識科練習 — 生物的分類（15分鐘車程版）
function createScienceForm() {
  var form = FormApp.create('常識科：生物的分類練習（15分鐘）');
  form.setIsQuiz(true);
  form.setShowLinkToRespondAgain(true);
  form.setCollectEmail(false);

  // Section 1: 兩棲類 vs 爬行類辨析
  form.addPageBreakItem().setTitle('Section 1: 兩棲類 vs 爬行類');
  
  addMC(form, '青蛙的皮膚特徵是什麼？', '濕潤無鱗', ['濕潤無鱗','乾燥有鱗片','長有羽毛','長有毛髮'], '💡 技巧-兩棲類：皮膚濕潤、無鱗片，用肺+皮膚呼吸');
  addMC(form, '蛇的皮膚特徵是什麼？', '乾燥有鱗片', ['乾燥有鱗片','濕潤無鱗','長有羽毛','有毛髮'], '💡 技巧-爬行類：皮膚乾燥、有鱗片，只用肺呼吸');
  addMC(form, '下列哪種動物屬於兩棲類？', '青蛙', ['青蛙','蛇','麻雀','大猩猩'], '💡 技巧-例子：青蛙、蠑螈是兩棲類；蛇、烏龜是爬行類');
  addMC(form, '下列哪種動物屬於爬行類？', '烏龜', ['烏龜','青蛙','金魚','麻雀'], '💡 技巧-例子：烏龜、蛇是爬行類；青蛙是兩棲類');
  addMC(form, '兩棲類和爬行類都用什麼器官呼吸？', '肺', ['肺','鰓','氣管','皮膚'], '💡 技巧-共同點：都用肺呼吸（但兩棲類還用皮膚輔助）');

  // Section 2: 脊椎動物 vs 無脊椎動物
  form.addPageBreakItem().setTitle('Section 2: 脊椎動物 vs 無脊椎動物');
  
  addMC(form, '下列哪種動物是脊椎動物？', '麻雀', ['麻雀','螞蟻','蝴蝶','蚯蚓'], '💡 技巧-脊椎動物：有脊柱，包括魚類、兩棲類、爬行類、鳥類、哺乳類');
  addMC(form, '下列哪種動物是無脊椎動物？', '螞', ['螞','金魚','青蛙','蛇'], '💡 技巧-無脊椎動物：無脊柱，如昆蟲類（螞、蝴蝶）');
  addMC(form, '脊椎動物共有幾個類別？', '5個', ['5個','4個','6個','3個'], '💡 技巧-記憶：魚類、兩棲類、爬行類、鳥類、哺乳類 = 5個');
  addMC(form, '昆蟲類屬於哪種動物？', '無脊椎動物', ['無脊椎動物','脊椎動物','兩棲類','爬行類'], '💡 技巧-昆蟲類沒有脊柱，屬於無脊椎動物');

  // Section 3: 植物分類
  form.addPageBreakItem().setTitle('Section 3: 植物分類');
  
  addMC(form, '百合屬於哪種植物？', '有花植物', ['有花植物','無花植物','水生植物','陸生植物'], '💡 技巧-有花植物：會開花結果，以種子繁殖，如百合、水仙');
  addMC(form, '松樹屬於哪種植物？', '無花植物', ['無花植物','有花植物','水生植物','苔蘚'], '💡 技巧-無花植物：不會開花，如松樹、蕨類、苔蘚');
  addMC(form, '松樹以什麼方式繁殖？', '以種子繁殖', ['以種子繁殖','以孢子繁殖','以根繁殖','以莖繁殖'], '⚠️ 注意：松樹是裸子植物，以種子繁殖（非孢子）');
  addMC(form, '蕨類以什麼方式繁殖？', '以孢子繁殖', ['以孢子繁殖','以種子繁殖','以根繁殖','以葉繁殖'], '💡 技巧-蕨類、苔蘚都以孢子繁殖');
  addMC(form, '下列哪種植物是水生植物？', '睡蓮', ['睡蓮','鳳凰木','百合','松樹'], '💡 技巧-水生植物：生長在水中，如睡蓮、水葫蘆');
  addMC(form, '下列哪種植物是陸生植物？', '鳳凰木', ['鳳凰木','睡蓮','水葫蘆','浮萍'], '💡 技巧-陸生植物：生長在陸地，如鳳凰木、樹木');

  // Section 4: 綜合應用
  form.addPageBreakItem().setTitle('Section 4: 綜合應用');
  
  addMC(form, '企鵝雖然不會飛，但它屬於哪種類別？', '鳥類', ['鳥類','哺乳類','兩棲類','爬行類'], '💡 技巧-關鍵特徵：有羽毛 + 卵生 = 鳥類（即使不會飛）');
  addMC(form, '鯨魚生活在海中，但它屬於哪種類別？', '哺乳類', ['哺乳類','魚類','兩棲類','爬行類'], '💡 技巧-關鍵特徵：胎生 + 用肺呼吸 = 哺乳類（不是魚類）');
  addMC(form, '下列哪組全部是脊椎動物？', '麻雀、金魚、青蛙', ['麻雀、金魚、青蛙','螞、蝴蝶、蚯蚓','松樹、蕨類、百合','睡蓮、鳳凰木、水葫蘆'], '💡 技巧-脊椎動物包含：魚類、兩棲類、爬行類、鳥類、哺乳類');
  addMC(form, '下列哪組全部是無脊椎動物？', '螞、蝴蝶、蚯蚓', ['螞、蝴蝶、蚯蚓','麻雀、蛇、青蛙','金魚、烏龜、大猩猩','百合、水仙、松樹'], '💡 技巧-無脊椎動物：昆蟲類、蠕蟲類等無脊柱動物');
  addMC(form, '有花植物和無花植物的主要分別是什麼？', '是否開花結果', ['是否開花結果','生長環境','是否有葉子','繁殖速度'], '💡 技巧-核心區別：有花植物會開花結果；無花植物永不開花');
}

// 輔助函數：添加選擇題
function addMC(form, question, correctAnswer, options, hint) {
  var item = form.addMultipleChoiceItem();
  item.setTitle(question + '\n' + hint);
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
