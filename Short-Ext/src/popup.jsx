import React, { useState } from 'react';
import { render } from 'react-dom';
import axios from 'axios';

function Popup() {
  const [urlInput, setUrlInput] = useState('');
  const [urlResponse, setUrlResponse] = useState('');
  const [submitText, setSubmitText] = useState('Shorten URL');

  function updateInput(e) {
    setUrlInput(e.target.value);
  }

  const postURL = async (e) => {
    e.preventDefault();
    const body = { url: e.target.url.value };
    try {
      axios
        .post('http://127.0.0.1:5000/', body)
        .then((response) => setUrlResponse(response.data))
        .then(setSubmitText('Shorten another URL'))
        .then(setUrlInput(''));
    } catch (error) {
      setUrlResponse('Sorry... the server is unavailable at this time');
      console.warn(error.message);
      setUrlInput('');
    }
  };

  return (
    <div>
      <h1>Shorten a URL!</h1>
      <div dangerouslySetInnerHTML={{ __html: `${urlResponse}` }} />
      <form onSubmit={postURL}>
        <input onChange={updateInput} type="url" name="url" value={urlInput} />
        <button type="submit">{submitText}</button>
      </form>
    </div>
  );
}

render(<Popup />, document.getElementById('react-target'));
