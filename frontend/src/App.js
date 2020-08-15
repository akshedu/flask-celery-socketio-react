import React from 'react';
import io from 'socket.io-client';
import { v4 as uuidv4 } from 'uuid';

import { serverUrl, port } from './config.js';
let socket = io.connect(`${serverUrl}:${port}`);
let room = uuidv4();

socket.on('connect', () => {
  socket.emit('join_room', room);
});

class App extends React.Component {

  constructor(props) {
     super(props);
     this.state = {
              post_body: '',
              result: null,
              processing: false
            }

     this.handleBodyChange = this.handleBodyChange.bind(this);
     this.handleSubmit = this.handleSubmit.bind(this);
   }

  componentDidMount() {
    socket.on('API_RESULT_AVAILABLE', (msg) => {
      this.setState({result: msg['data'] || 'null'})
    });
  }

   handleBodyChange(event) {
     this.setState({post_body: event.target.value});
   }

   handleSubmit() {
    this.setState({processing: true});
     fetch(`${serverUrl}:${port}/external?room=${room}`, {
      method: "POST",
      headers: {
          "Content-Type":"application/json",
      },
      body: JSON.stringify(this.state.post_body)
      }
  ).catch(function(err) {
    console.info(err);
  });}

  renderResult() {
    if (this.state.result) {
      return (
            <p>
              Output: {this.state.result}
            </p>
      );
    }
  }

  render() {
     return (
       <div>
         <h1> Enter the data to be sent to post request </h1>
         <input type="text" name="post_body" value={this.state.post_body} onChange={this.handleBodyChange} />
         <button onClick={this.handleSubmit}>POST</button>
         {this.state.processing && <h1>Processing</h1>}
         {this.renderResult()}
       </div>
     );
   }
}

export default App;
