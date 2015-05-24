angular.module('mount_calculator', []).controller('MountCalculator', function(){
    this.p = 1.00;  //chance
    this.k = 1;     //number of drops
    this.n = 100;   //number of kills

    //binomial distribution
    this.drop_chance = function drop_chance_f(k, n, p){
        p = p/100
        var result = binom(n, k) * Math.pow(p, k) * Math.pow((1 - p), (n - k))

        result = result * 100;
        result = Math.round(result * 1000) / 1000; //3 decimals

        return (result + "%");
    };

    this.drop_chance_one = function drop_chance_f(k, n, p){
        p = p/100
        var result = binom(n, k) * Math.pow(p, k) * Math.pow((1 - p), (n - k))

        result = 1- result;
        result = result * 100;
        result = Math.round(result * 1000) / 1000;

        return (result + "%");
    };

    //http://rosettacode.org/wiki/Evalate_binomial_coefficients#JavaScript
    function binom(n, k) {
        var coeff = 1;
        for (var i = n-k+1; i <= n; i++) coeff *= i;
        for (var i = 1;     i <= k; i++) coeff /= i;
        return coeff;
    }
});