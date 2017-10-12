var exports = require('./exports')
var setup = require('./setup')

var web3 = exports.web3
var vulnerableContracts = exports.web3
setup.go().then(function () {
  console.log(vulnerableContracts)
})


