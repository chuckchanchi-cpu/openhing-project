// Justan 英文薄弱項訓練 — 從文章中找詞填空 (2026-09-18)
function createVocabFromTextForm() {
  var form = FormApp.create('英文填空訓練 — 從文章中找詞 (2026-09-18)');
  form.setIsQuiz(true);
  form.setShowLinkToRespondAgain(false);
  form.setCollectEmail(false);

  // Section 1: Pet Adoption Article
  form.addPageBreakItem().setTitle('Section 1: Pet Adoption（領養寵物）');
  
  addShortAnswer(form, 'Article: "Get Ready to Meet Your New Family Member!"\n\nIf you want a pet, you can save money and _____(1) one from an animal shelter. Animal shelters rescue stray pets from the streets. Once you have a pet, you must be _____(2) its care. You should never _____(3) it when it gets old or sick.\n\nWord Bank: abandon / adopt / responsible for', 'adopt', '💡 提示：save money and ___ one → 領養一個');
  addShortAnswer(form, 'Article: "Get Ready to Meet Your New Family Member!"\n\nIf you want a pet, you can save money and _____(1) one from an animal shelter. Animal shelters rescue stray pets from the streets. Once you have a pet, you must be _____(2) its care. You should never _____(3) it when it gets old or sick.\n\nWord Bank: abandon / adopt / responsible for', 'responsible for', '💡 提示：be ___ its care → 對它的照顧負責');
  addShortAnswer(form, 'Article: "Get Ready to Meet Your New Family Member!"\n\nIf you want a pet, you can save money and _____(1) one from an animal shelter. Animal shelters rescue stray pets from the streets. Once you have a pet, you must be _____(2) its care. You should never _____(3) it when it gets old or sick.\n\nWord Bank: abandon / adopt / responsible for', 'abandon', '💡 提示：never ___ it → 永遠不要拋棄它');
  addShortAnswer(form, 'Article: "Get Ready to Meet Your New Family Member!"\n\nPuppies and kittens are lovely, but they might scratch the furniture or make a mess while you are out. An adult animal will be more _____(4) for you because they are calmer. Before adopting, you need to complete an _____(5).\n\nWord Bank: suitable / application form', 'suitable', '💡 提示：more ___ for you → 更適合你');
  addShortAnswer(form, 'Article: "Get Ready to Meet Your New Family Member!"\n\nPuppies and kittens are lovely, but they might scratch the furniture or make a mess while you are out. An adult animal will be more _____(4) for you because they are calmer. Before adopting, you need to complete an _____(5).\n\nWord Bank: suitable / application form', 'application form', '💡 提示：complete an ___ → 完成申請表');
  addShortAnswer(form, 'Article: "Get Ready to Meet Your New Family Member!"\n\nAfter adopting, a vet will give your pet a health check. You also need to take your pet for _____(6) at the vet\'s clinic. Finally, you must apply for a dog licence within three months.\n\nWord Bank: injections / dog licence / health check', 'injections', '💡 提示：take your pet for ___ → 帶寵物打疫苗');

  // Section 2: Environmental Protection Article
  form.addPageBreakItem().setTitle('Section 2: Environmental Protection（環保）');
  
  addShortAnswer(form, 'Article: "Protect Our Planet"\n\nOur Earth is facing many environmental problems. Air pollution is caused by factories and cars. Water pollution happens when people throw trash into rivers. We must be _____(1) for our planet.\n\nWord Bank: responsible / dangerous / suitable', 'responsible', '💡 提示：be ___ for our planet → 對地球負責');
  addShortAnswer(form, 'Article: "Protect Our Planet"\n\nWe can help by recycling paper, plastic, and glass. We should also _____(2) water by turning off the tap when we brush our teeth.\n\nWord Bank: waste / save / pollute', 'save', '💡 提示：___ water → 節約用水');
  addShortAnswer(form, 'Article: "Protect Our Planet"\n\nPlanting trees is another good way to help. Trees clean the air and provide homes for animals. Every small action counts! Let us work together to make our world a better place.\n\nWord Bank: destroy / protect / abandon', 'protect', '💡 提示：work together to ___ our world → 保護世界');

  // Section 3: School Life Article
  form.addPageBreakItem().setTitle('Section 3: School Life（學校生活）');
  
  addShortAnswer(form, 'Article: "A Day at School"\n\nEvery morning, I go to school with my friends. We sit in the classroom and listen to our teachers. My favourite subject is English because I like to read stories and write essays.\n\nWord Bank: boring / favourite / difficult', 'favourite', '💡 提示：My ___ subject → 我最喜歡的科目');
  addShortAnswer(form, 'Article: "A Day at School"\n\nAt break time, we play games on the playground. Some students run around, while others sit under the trees and talk. After lunch, we have science class. We do experiments and learn about different things.\n\nWord Bank: interesting / terrible / awful', 'interesting', '💡 提示：We do experiments and learn → 實驗很有趣');
}

// 輔助函數：添加短答題
function addShortAnswer(form, question, correctAnswer, hint) {
  var item = form.addShortAnswerItem();
  item.setTitle(question + '\n' + hint);
  item.setRequired(true);
  
  item.setFeedbackForCorrectResponse(
    FormApp.createFeedback().setFeedbackText('✅ Correct! Well done!')
  );
  item.setFeedbackForIncorrectResponse(
    FormApp.createFeedback().setFeedbackText('❌ Wrong! The answer is: ' + correctAnswer)
  );
}
