var observations = [0.,30.,50.,100.,100.,75.,200.,20.,10.,0.];

var n_states = 3;

var mus = [0.,100.,50.];
var sigmas = [20.,20.,20.];

var start_prob = [.33,.33,.34];
var start_prob = start_prob.map(function(x, i) {
    return - Math.log(x);
});
var trans_prob = [[.9,.05,.05],[.1,.8,.1],[.2,.2,.6]];
var trans_prob = trans_prob.map(function(x, i) {
    return - Math.log(x);
});

function norm_pdf(X,mu,sigma) {
    return X.map(function(x,i) {
        return -Math.log(Math.exp(-(x-mu)^2/2/(sigma^2))/Math.sqrt(2*Math.PI)/sigma);
    });
}

function state_probabilities(observations,mus,sigmas) {
    var state_probs = [];
    for (i = 0; i < n_states; i++) {
        state_probs.push(norm_pdf(observations,mus[i],sigmas[i]));
    }
    return state_probs;
}

state_probs = state_probabilities(observations,mus,sigmas);

console.log(state_probs)
