const express = require('express')
const jieba = require('nodejieba')
const Sequelize = require('sequelize')
const fs = require('fs')

const sequelize = new Sequelize('mysql://root:password@localhost:3306/se')


const server = express()
server.listen(8080)

const allowCrossDomain = function(req,res,next) {
  res.header('Access-Control-Allow-Origin', '*')
  next();
}

server.use(allowCrossDomain)


function getResult(res,sw) {
  let mark
  let result = []
  let temp
  for (var i = 0; i < res.length; i++) {
    mark = 0
    temp = {}
    for (let j = 0; j < sw.length; j++) {
      if (res[i][sw[j].word]) {
        mark += parseFloat(res[i][sw[j].word]) * sw[j].weight
      }
    }
    temp.filename = res[i].filename
    temp.rank = mark
    temp.id = res[i].id
    result.push(temp)
  }
  // console.log(res)
  return result
}

function getCondition(words) {
  let condition = ''
  for (var i = 0; i < words.length; i++) {
    if (i !== words.length-1) {
      condition += `'${words[i].word}',`
    } else {
      condition += `'${words[i].word}'`
    }
  }
  return condition
}

function compare(prop) {
  return function(a,b) {
    var val1 = a[prop]
    var val2 = b[prop]
    return val2 - val1
  }
}

server.get('/se',(req,res)=>{
  //只接受前19个字符
  let con = req.query.inputCon.substring(0,19)
  let words = jieba.extract(con,10)

  // console.info(words)

  let condition = getCondition(words)
  // console.log(condition)

  let i, k
  let temp
  let urls = ''
  let reg = new RegExp("\r\n");
  const names = []
  const objs = []
  const fns = [] //filenames

  sequelize.query(`SELECT * FROM tfidf WHERE word IN (${condition})`, { type: sequelize.QueryTypes.SELECT})
  .then(result => {
    for (i = 0; i < result.length; i++) {
      if (names.indexOf(result[i].filename) === -1) {
        let temp = {}
        names.push(result[i].filename)
        temp.filename = result[i].filename
        temp[result[i].word] = result[i].tfidf
        // console.log(result[i].id)
        temp.id = result[i].id
        objs.push(temp)
      }
    }

    //通过tfidf计算并获得相关度最高的前10篇文章
    processedResult = getResult(objs,words).sort(compare('rank')).slice(0,10)

    //记录排名前十的文件名
    for (i = 0; i < processedResult.length; i++) {
      fns.push(processedResult[i].filename)
    }

    for (i = 0; i < processedResult.length; i++) {
      fileContent = fs.readFileSync(`../docs/target/${processedResult[i].filename}`,'utf-8')
      processedResult[i].title = fileContent.split('\r\n')[1].substring(7)
      fileContent = fileContent.substring(fileContent.indexOf('content'))
      fileContent = fileContent.replace(reg," ");
      fileContent = fileContent.replace(/\s+/g, ' ');
      // console.log(fileContent)
      processedResult[i].con = fileContent.substring(9,100)
    }
    
    for (k = 0; k < fns.length; k++) {
      if (k !== fns.length-1) {
        urls += `'${fns[k]}',`
      } else {
        urls += `'${fns[k]}'`
      }
    }
    // console.log(urls)

    sequelize.query(`SELECT * FROM files WHERE name IN (${urls})`, { type: sequelize.QueryTypes.SELECT})
    .then(urlResult => {
      for (i = 0; i < processedResult.length; i++ ) {
        for (k = 0; k < urlResult.length; k++ ) {
          if (processedResult[i].filename === urlResult[k].name) {
            processedResult[i].url = urlResult[k].url
          }
        }
      }
      // console.info(processedResult)
      res.send({
        processedResult,
        words
      })
    })
    .catch(err => {
      console.log('get urls failed')
      res.send('get urls failed')
    })

  })
  .catch(err => {
    res.send('db connection error')
    console.log('error!')
  })
})