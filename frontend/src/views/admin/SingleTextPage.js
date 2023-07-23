import React, { useState, useEffect } from "react";
import { useParams } from 'react-router-dom';

// components

import CardTextDetail from "components/Cards/CardTextDetail";
import CardAuthorProfile from "components/Cards/CardAuthorProfile.js";

export default function SingleTextPage() {
  let { text_id } = useParams();
  const [text, setText] = useState(null);

  useEffect(() => {
    if (text_id) {
      fetch(`http://localhost:8000/texts/${text_id}`)
        .then(response => response.json())
        .then(data => {
          setText(data);
        })
        .catch(err => console.error(err));
    }
  }, [text_id]);

  if (!text) {
    return <div>Loading...</div>;
  }

  return (
    <>
      <div className="flex flex-wrap">
        <div className="w-full lg:w-8/12 px-4">
          <CardTextDetail text={text} />
        </div>
        <div className="w-full lg:w-4/12 px-4">
          <CardAuthorProfile author={text.author} author_id={text.author_id} />
        </div>
        
      </div>
    </>
  );
}
