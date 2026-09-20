// 中文填充練習 — Chapter 8 詞語 (2026-09-17)
function createChapter8Form() {
  var form = FormApp.create('中文填充練習 — Chapter 8 詞語 (2026-09-17)');
  form.setIsQuiz(true);
  form.setShowLinkToRespondAgain(false);
  form.setCollectEmail(false);

  // Section 1: 基礎填充（簡單）
  form.addPageBreakItem().setTitle('Section 1: 基礎填充');
  
  addShortAnswer(form, '他做事非常________，即使遇到困難也不會放棄。', '執著', '💡 執著 = 堅持不懈');
  addShortAnswer(form, '面對挫折，他不應________，而應該勇敢面對。', '退縮', '💡 退縮 = 畏懼困難而後退');
  addShortAnswer(form, '做任何事都不能________，要經過深思熟慮。', '蠻幹', '💡 蠻幹 = 不講方法地硬幹');
  addShortAnswer(form, '兩人的看法________不同，誰也說服不了誰。', '迥然', '💡 迥然 = 明顯不同的樣子');
  addShortAnswer(form, '看到這個結果，他不禁________不已。', '感嘆', '💡 感嘆 = 感慨嘆息');
  addShortAnswer(form, '我們不能向困難________，要勇往直前。', '屈服', '💡 屈服 = 順從、投降');
  addShortAnswer(form, '他________的精神值得我們學習。', '百折不回', '💡 百折不回 = 經歷多次挫折也不退縮');
  addShortAnswer(form, '遇到困難就________，這樣永遠不會成功。', '自暴自棄', '💡 自暴自棄 = 自己輕視自己，不求上進');
  addShortAnswer(form, '他常常________，抱怨命運不公。', '嘆氣', '💡 嘆氣 = 因憂愁、傷感等而呼氣');
  addShortAnswer(form, '不要________行事，要根據實際情況做決定。', '盲目', '💡 盲目 = 沒有目的、沒有主見');

  // Section 2: 進階應用（中等）
  form.addPageBreakItem().setTitle('Section 2: 進階應用');
  
  addShortAnswer(form, '經過老師的教導，他________到自己的錯誤。', '反省', '💡 反省 = 自我檢討、反思');
  addShortAnswer(form, '這種行為實在太________了，令人痛心。', '可悲', '💡 可悲 = 值得同情、令人悲哀');
  addShortAnswer(form, '每個人對這件事都有不同的________。', '觀點', '💡 觀點 = 看問題的角度、立場');
  addShortAnswer(form, '天氣________暖和起來，春天來了。', '稍微', '💡 稍微 = 略微、一點點');
  addShortAnswer(form, '生活總會有________，我們要學會適應。', '改變', '💡 改變 = 變化、轉變');
  addShortAnswer(form, '這段經歷給了我很大的________，讓我成長了很多。', '啟示', '💡 啟示 = 領悟的道理、教訓');

  // Section 3: 綜合挑戰（困難）
  form.addPageBreakItem().setTitle('Section 3: 綜合挑戰');
  
  addShortAnswer(form, '雖然遇到了很多困難，但他依然________，最終達成了目標。', '百折不回', '💡 百折不回 + 執著 = 堅持不懈的精神');
  addShortAnswer(form, '如果一個人總是________，只會讓身邊的人更加________。', '自暴自棄', '💡 自暴自棄 → 可悲');
  addShortAnswer(form, '面對不同的________，我們應該保持開放的心態，不要________。', '觀點', '💡 觀點不同 → 不要盲目跟從');
}

// 輔助函數：添加短答題
function addShortAnswer(form, question, correctAnswer, hint) {
  var item = form.addShortAnswerItem();
  item.setTitle(question + '\n' + hint);
  item.setRequired(true);
  
  item.setFeedbackForCorrectResponse(
    FormApp.createFeedback().setFeedbackText('✅ Correct!')
  );
  item.setFeedbackForIncorrectResponse(
    FormApp.createFeedback().setFeedbackText('❌ Wrong! The answer is: ' + correctAnswer)
  );
}
