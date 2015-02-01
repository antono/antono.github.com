var inputElement, outputElement;

var charMap = {
    ' ': ' ',
    'А': 'A',
    'Б': 'B',
    'В': 'V',
    'Г': 'G',
    'Д': 'D',
    'Ж': 'ZH',
    'З': 'Z',
    'И': 'I',
    'Й': 'Y',
    'К': 'K',
    'Л': 'L',
    'М': 'M',
    'Н': 'N',
    'О': 'O',
    'П': 'P',
    'Р': 'R',
    'С': 'S',
    'Т': 'T',
    'У': 'U',
    'Ф': 'F',
    'Х': 'KH',
    'Ц': 'TS',
    'Ч': 'CH',
    'Ш': 'SH',
    'Щ': 'SHCH',
    'Ъ': '',
    'Ы': 'Y',
    'Ь': '',
    'Э': 'E',
    'Ю': 'YU',
    'Я': 'YA'
}

var preYe = 'АЕЁИОУЪЫЬЭЮЯ'.split('');

var transliterate = function(input) {
    var result, prev = null, arr = input.split("");

    result = arr.map(function (inChar) {
        var outChar;

        char = inChar.toUpperCase();

        if (['Е','Ё'].indexOf(char) != -1) {
            if (!prev || preYe.indexOf(prev) != -1) {
                return 'YE';
            } else {
                return 'E';
            }
        }

        res = charMap[char];

        if (res === undefined) {
            throw Error("Unknown char: " + inChar);
        }

        prev = char;

        return res;
    });


    return result.join('');
};

var processInput = function() {
    outputElement.value = transliterate(inputElement.value);
};

var toggleHelp = function() {
    document.getElementById('rules').classList.toggle('hidden');
};

window.addEventListener("load", function load(event){

    inputElement  = document.getElementById('inString');
    outputElement = document.getElementById('outString');

    document.getElementById('inString').addEventListener('change', processInput);
    document.getElementById('processButton').addEventListener('click', processInput);
    document.getElementById('helpButton').addEventListener('click', toggleHelp);

    window.removeEventListener("load", load, false); //remove listener, no longer needed

}, false);
