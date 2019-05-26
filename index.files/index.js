let dict, wordCount = 0, correctCount = 0;

const loadedDict = (async () => {
	const response = await fetch('index.files/kunyomi.json');
	if (!response.ok)
		swal('Error', 'Cannot fetch dictionary!', 'error');
	else
		dict = await response.json();
})()

const refreshBoard = () => {
	const words = Object.keys(dict)
		, randNum = Math.random() * words.length | 0;
	wordLabel.innerText = words[randNum];
	scoreOutput.innerText = `正解 ${correctCount} 総数 ${wordCount++}`;
}

(async () => {
	await loadedDict;
	refreshBoard();
})()

const wordTransformer = answer => answer.replace('-', '');

const handleYomikataInput = () => {
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
