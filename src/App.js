import React from 'react';
import './App.css'
import axios from './axios'


class App extends React.Component {

  constructor(){
    super()
    this.state = {
      inputCon: null,
      isFocused: false,
      resultCon: [],
      words: [],
    }
  }

  componentDidMount(){
    document.addEventListener("keydown",this.handleEnterKey)
    let ps = document.getElementsByClassName('item-content')
    console.info(ps)
  }

  componentWillUmount(){
    document.removeEventListener("keydown",this.handleEenterKey)
  }

  handleEnterKey = (e) => {
    if(e.keyCode === 13 && this.state.isFocused === true){
      axios.get('/se',{
        params: {
          inputCon: this.state.inputCon
        }
      })
      .then(res=>{
        console.log(res.data.processedResult)
        this.setState({
          resultCon: res.data.processedResult,
          words: res.data.words
        })
      })
      .catch(err=>{
        console.log(err)
      })
    }
  }

  handleInputChange(e){
    let inputCon = e.target.value
    this.setState({
      inputCon
    })
  }

  getFocus() {
    this.setState({
      isFocused: true
    })
  }

  loseFocus() {
    this.setState({
      isFocused: false
    })
  }

  render() {
    let {resultCon, words} = this.state
    if (words) {
      for (let i = 0; i < words.length; i++) {
        resultCon.filter((value,index) => { //使用filter函数过滤新闻列表数据
          var re =new RegExp(words[i].word,"g"); //定义正则
          value.con=value.con.replace(re, `<span class="hl">${words[i].word}</span>`); //进行替换，并定义高亮的样式
          value.title=value.title.replace(re, `<span class="hl">${words[i].word}</span>`); //进行替换，并定义高亮的样式
        })
      }
    }
    return (
      <div className="App">
        <header>
          <div className="main-input">
            <input id='getSearchContent' 
                   autoFocus
                   autoComplete = 'off'
                   onFocus={this.getFocus.bind(this)}
                   onBlur={this.loseFocus.bind(this)}
                   className='ipt'
                   type="text"
                   onChange={this.handleInputChange.bind(this)}
            />
          </div>
        </header>
        <section>
          {
            resultCon
            ? resultCon.map((item,i)=>
              <div key={i} className='item'>
                <a rel="stylesheet" href={item.url} target='block' dangerouslySetInnerHTML = {{ __html:item.title}}></a>
                <p className='item-content' dangerouslySetInnerHTML = {{ __html:item.con+'...' }}></p>
              </div>
            )
            : <p className='hl failed'><span>QAQ</span>sorry, but match failed </p>
          }
        </section>
      </div>

    )
  }
}

export default App;

