// 英文默書複習 — 職業詞語 (2026-09-17)
function createVocabularyForm() {
  var form = FormApp.create('英文默書複習 — 職業詞語 (2026-09-17)');
  form.setIsQuiz(true);
  form.setShowLinkToRespondAgain(false);
  form.setCollectEmail(false);

  // Section 1: 核心20個必背職業（MC）
  form.addPageBreakItem().setTitle('Section 1: 核心20個必背職業');
  
  addMC(form, '創作出音樂的人', 'composer', ['composer','conductor','director','writer'], '💡 composer = 作曲家，把音符放在一起');
  addMC(form, '跳舞的人', 'dancer', ['dancer','singer','actor','painter'], '💡 dancer = 舞者，dance + -er');
  addMC(form, '設計衣服款式的人', 'fashion designer', ['fashion designer','tailor','seamstress','model'], '💡 fashion designer = 時尚設計師');
  addMC(form, '剪頭髮、做造型的人', 'hairdresser', ['hairdresser','barber','stylist','cosmetologist'], '💡 hairdresser = 美髮師，hair + dress + -er');
  addMC(form, '畫畫的人', 'painter', ['painter','artist','illustrator','sculptor'], '💡 painter = 畫家，paint + -er');
  addMC(form, '拍照的人', 'photographer', ['photographer','cameraman','journalist','reporter'], '💡 photographer = 攝影師，photo + graph + -er');
  addMC(form, '唱流行歌曲的人', 'pop singer', ['pop singer','rock star','rapper','musician'], '💡 pop singer = 流行歌手');
  addMC(form, '為慈善機構工作的人', 'charity worker', ['charity worker','volunteer','NGO worker','social worker'], '💡 charity worker = 義工，charity + worker');
  addMC(form), ['空服員在飛機上服務乘客的人', 'flight attendant', ['flight attendant','steward','pilot','passenger'], '💡 flight attendant = 空服員，flight + attend'];
  addMC(form, '滅火的人', 'fireman', ['fireman','firefighter','police officer','rescuer'], '💡 fireman = 消防員，fire + man');
  addMC(form, '維持治安的人', 'policeman', ['policeman','guard','detective','soldier'], '💡 policeman = 警察，police + man');
  addMC(form, '送信件的人', 'postman', ['postman','messenger','courier','delivery man'], '💡 postman = 郵差，post + man');
  addMC(form, '賣東西的人', 'salesman', ['salesman','vendor','merchant','shopkeeper'], '💡 salesman = 銷售員，sale + man');
  addMC(form, '看牙齒的醫生', 'dentist', ['dentist','doctor','surgeon','physician'], '💡 dentist = 牙醫，dent + ist');
  addMC(form, '做飯的人', 'chef', ['chef','cook','baker','waiter'], '💡 chef = 廚師，法語原詞，特殊拼寫');
  addMC(form, '報導新聞的人', 'reporter', ['reporter','journalist','correspondent','editor'], '💡 reporter = 記者，report + -er');
  addMC(form, '寫書/文章的人', 'writer', ['writer','author','novelist','poet'], '💡 writer = 作家，write + -r');
  addMC(form, '修改、整理內容的人', 'editor', ['editor','publisher','proofreader','reviewer'], '💡 editor = 編輯，edit + -or');
  addMC(form, '畫圖解說明書的人', 'illustrator', ['illustrator','artist','designer','cartoonist'], '💡 illustrator = 插畫家，illustrate + -tor');
  addMC(form, '演戲的人', 'actor', ['actor','actress','performer','player'], '💡 actor/actress = 演員，act + -or/-ess');

  // Section 2: 表演與娛樂類（MC）
  form.addPageBreakItem().setTitle('Section 2: 表演與娛樂類');
  
  addMC(form, '指導拍電影的人', 'film director', ['film director','movie maker','producer','screenwriter'], '💡 film director = 電影導演，film + direct + -or');
  addMC(form, '展示服裝、拍照的人', 'model', ['model','mannequin','poseur','displayer'], '💡 model = 模特兒');
  addMC(form, '特別喜歡某件收藏品的人', 'collector', ['collector','curator','archivist','preserver'], '💡 collector = 收藏家');

  // Section 3: 額外16個職業（MC）
  form.addPageBreakItem().setTitle('Section 3: 額外16個職業');
  
  addMC(form, '設計建築物的人', 'architect', ['architect','builder','constructor','engineer'], '💡 architect = 建築師');
  addMC(form, '去太空的人', 'astronaut', ['astronaut','cosmonaut','space traveler','pilot'], '💡 astronaut = 太空人');
  addMC(form, '參加體育比賽的人', 'athlete', ['athlete','sportsman','competitor','champion'], '💡 athlete = 運動員');
  addMC(form, '收錢的人', 'cashier', ['cashier','teller','bank clerk','accountant'], '💡 cashier = 收銀員');
  addMC(form, '解決技術問題的人', 'engineer', ['engineer','technician','mechanic','developer'], '💡 engineer = 工程師');
  addMC(form, '審判案件的人', 'judge', ['judge','magistrate','arbitrator','referee'], '💡 judge = 法官');
  addMC(form, '提供法律帮助的人', 'lawyer', ['lawyer','attorney','counsel','barrister'], '💡 lawyer = 律師');
  addMC(form, '保護水中安全的人', 'lifeguard', ['lifeguard','swimming instructor','rescuer','coast guard'], '💡 lifeguard = 救生員');
  addMC(form, '開飛機的人', 'pilot', ['pilot','aviator','flyer','navigator'], '💡 pilot = 飛行員');
  addMC(form, '國家的最高領導人', 'president', ['president','leader','monarch','prime minister'], '💡 president = 總統');
  addMC(form, '帶遊客參觀的人', 'tour guide', ['tour guide','travel agent','host','hostess'], '💡 tour guide = 導遊');
  addMC(form, '看動物病的醫生', 'vet', ['vet','veterinarian','animal doctor','zookeeper'], '💡 vet = 獸醫，veterinary doctor 簡寫');
  addMC(form, '彈鋼琴的人', 'pianist', ['pianist','keyboardist','musician','composer'], '💡 pianist = 鋼琴家，piano + -ist');
  addMC(form, '拉小提琴的人', 'violinist', ['violinist','musician','orchestra member','conductor'], '💡 violinist = 小提琴家，violin + -ist');
  addMC(form, '做生意的人', 'businessman', ['businessman','entrepreneur','merchant','trader'], '💡 businessman = 商人，business + man');
  addMC(form, '管理公司/商店的人', 'manager', ['manager','supervisor','administrator','director'], '💡 manager = 總管，manage + -er');

  // Section 4: 快速填充測試（填空題）
  form.addPageBreakItem().setTitle('Section 4: 快速填充測試');
  
  addShortAnswer(form, '創作出音樂的人是________', 'composer', '💡 composer = 作曲家');
  addShortAnswer(form, '剪頭髮的人是________', 'hairdresser', '💡 hairdresser = 美髮師');
  addShortAnswer(form, '滅火的人是________', 'fireman', '💡 fireman = 消防員');
  addShortAnswer(form, '送信件的人是________', 'postman', '💡 postman = 郵差');
  addShortAnswer(form, '看牙齒的醫生是________', 'dentist', '💡 dentist = 牙醫');
  addShortAnswer(form, '做飯的人是________', 'chef', '💡 chef = 廚師');
  addShortAnswer(form, '寫書的人是________', 'writer', '💡 writer = 作家');
  addShortAnswer(form, '演戲的人是________', 'actor', '💡 actor = 演員');
  addShortAnswer(form, '去太空的人是________', 'astronaut', '💡 astronaut = 太空人');
  addShortAnswer(form, '看動物病的醫生是________', 'vet', '💡 vet = 獸醫');
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
