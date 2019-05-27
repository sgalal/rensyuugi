let dict, wordCount, correctCount;

const loadedDict = async dictUrl => {
	const response = await fetch(dictUrl);
	if (!response.ok)
		swal('Error', 'Cannot fetch dictionary!', 'error');
	else
		dict = await response.json();
}

const refreshBoard = () => {
	const words = Object.keys(dict)
		, randNum = Math.random() * words.length | 0;
	wordLabel.innerText = words[randNum];
	scoreOutput.innerText = `正解 ${correctCount} 総数 ${wordCount++}`;
}

const handleYomikataInput = wordTransformer => async () => {
	if (dict[wordLabel.innerText].map(wordTransformer).includes(yomikataInput.value)) {
		yomikataInput.value = "";
		++correctCount;
		refreshBoard();
	}
}

const handleSkip = async () => {
	await swal(dict[wordLabel.innerText].join(', '), { buttons: { cancel: "OK" } });
	yomikataInput.value = "";
	refreshBoard();
}

const handleSelectChange = async () => {
	const selectValue = document.querySelector('select').value;
	if (selectValue == 'kunyomi') {
		wordCount = 0, correctCount = 0;

		await loadedDict('index.files/kunyomi/data.json');
		document.querySelector('form').lang = 'ja-JP';
		refreshBoard();

		const wordTransformer = answer => answer.replace('-', '');
		yomikataInput.addEventListener('input', handleYomikataInput(wordTransformer));
		skipButton.addEventListener('click', handleSkip);
	} else if (selectValue == 'hanjaeo') {
		wordCount = 0, correctCount = 0;

		await loadedDict('index.files/hanjaeo/data.json');
		document.querySelector('form').lang = 'ko';
		refreshBoard();

		const wordTransformer = answer => answer;
		yomikataInput.addEventListener('input', handleYomikataInput(wordTransformer));
		skipButton.addEventListener('click', handleSkip);
	}
}

window.addEventListener('DOMContentLoaded', handleSelectChange);
