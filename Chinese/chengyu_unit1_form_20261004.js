// 中文填充練習 — 成語單元一 (2026-10-04)
function createChengyuForm() {
  var form = FormApp.create('中文填充練習 — 成語單元一 (2026-10-04)');
  form.setIsQuiz(true);
  form.setShowLinkToRespondAgain(false);
  form.setCollectEmail(false);

  // Section 1: 基礎填充（從詞彙表選詞）
  form.addPageBreakItem().setTitle('Section 1: 基礎填充');
  
  addShortAnswer(form, '這座古寺歷經百年風霜，如今已________，只剩下幾根殘柱。', '碩果僅存', '💡 碩果僅存：大而豐厚的成果只剩很少');
  addShortAnswer(form, '節假日的尖沙咀________，遊客絡繹不絕。', '車水馬龍', '💡 車水馬龍：形容車輛很多，來往不斷');
  addShortAnswer(form, '演出開始後，觀眾________，場面秩序井然。', '魚貫而入', '💡 魚貫而入：像魚一樣一個接一個地進入');
  addShortAnswer(form, '人工智能技術________，每年都有重大突破。', '日新月異', '💡 日新月異：每天每月都有新變化，形容發展迅速');
  addShortAnswer(form, '犯罪份子作案後立即________，警方苦無線索。', '消聲匿跡', '💡 消聲匿跡：隱蔽起來，不露痕跡');
  addShortAnswer(form, '這位年輕設計師的作品________，在展覽中格外搶眼。', '別樹一幟', '💡 別樹一幟：獨創一格，與眾不同');
  addShortAnswer(form, '經濟復甦後，創新企業如________般大量出現。', '雨後春筍', '💡 雨後春筍：比喻新生事物大量湧現');
  addShortAnswer(form, '他的收藏品價值連城，一向自恃________，不肯輕易出手。', '奇貨可居', '💡 奇貨可居：把珍貴的東西囤積起來，等待高價出售');
  addShortAnswer(form, '這座危樓年久失修，隨時可能倒塌，真是________。', '搖搖欲墜', '💡 搖搖欲墜：形勢危險，快要倒塌或垮台');
  addShortAnswer(form, '該區人口稀疏，商店寥寥無幾，幾乎是________。', '門可羅雀', '💡 門可羅雀：門前可以張網捕雀，形容十分冷落');
  addShortAnswer(form, '演唱會現場________，歌迷熱情高涨。', '座無虛席', '💡 座無虛席：座位都坐滿了，形容參加的人很多');
  addShortAnswer(form, '他家境貧寒，每月收入只夠糊口，常常________。', '捉襟見肘', '💡 捉襟見肘：形容貧困或處境困難，應付不過來');
  addShortAnswer(form, '在莊嚴的紀念儀式上，有人嬉笑打鬧，實在是________。', '大煞風景', '💡 大煞風景：破壞美好的景色或氣氛');
  addShortAnswer(form, '這朵昙花开放时间極短，只是________，令人惋惜。', '曇花一現', '💡 曇花一現：比喻美好事物短暫出現就消失');

  // Section 2: 進階應用（造句填空）
  form.addPageBreakItem().setTitle('Section 2: 進階應用');
  
  addShortAnswer(form, '請用「車水馬龍」造句：描述一個繁忙的城市街道場景。', '', '💡 提示：使用「車水馬龍」形容車輛很多，來往不斷');
  addShortAnswer(form, '請用「別樹一幟」造句：描述一位藝術家的獨特風格。', '', '💡 提示：使用「別樹一幟」形容獨創一格，與眾不同');
  addShortAnswer(form, '請用「大煞風景」造句：描述一個破壞美好氣氛的行為。', '', '💡 提示：使用「大煞風景」形容破壞美好的景色或氣氛');
}

// 輔助函數：添加短答題
function addShortAnswer(form, question, correctAnswer, hint) {
  var item = form.addShortAnswerItem();
  item.setTitle(question + '\n' + hint);
  item.setRequired(true);
  
  if (correctAnswer) {
    item.setFeedbackForCorrectResponse(
      FormApp.createFeedback().setFeedbackText('✅ Correct!')
    );
    item.setFeedbackForIncorrectResponse(
      FormApp.createFeedback().setFeedbackText('❌ Wrong! The answer is: ' + correctAnswer)
    );
  }
}
