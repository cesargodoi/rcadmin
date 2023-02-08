const exceptions = [
    "00000000000",
    "11111111111",
    "22222222222",
    "33333333333",
    "44444444444",
    "55555555555",
    "66666666666",
    "77777777777",
    "88888888888",
    "99999999999",
]

const w1 = [10, 9, 8, 7, 6, 5, 4, 3, 2];

const w2 = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2];

function calcDigit(cpf){
    let getSum = 0;
    if (cpf.length === 9) {
        var i = 0;
        while (i < w1.length) {
            getSum += cpf[i] * w1[i];
            i++;
        } 
    } else {
        var i = 0;
        while (i < w2.length) {
            getSum += cpf[i] * w2[i];
            i++;
        }
    }
    const partial = 11 - (getSum % 11);

    return partial > 9 ? 0 : partial;
}


function cpfValidation(num) {
    let cpf = num.toString().replace(/[^0-9]/g, '');

    if (cpf.length !== 11 || exceptions.includes(cpf)) {
        return false
    }

    cpf = cpf.split('').map(i => parseInt(i))

    if (cpf[9] !== calcDigit(cpf.slice(0,9))) {
        return false
    }

    if (cpf[10] !== calcDigit(cpf.slice(0,10))) {
        return false
    }

    return true
}
