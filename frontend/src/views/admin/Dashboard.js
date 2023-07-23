import React, { useState, useEffect } from "react";
import { useParams } from 'react-router-dom';
import AuthorTexts from "components/Cards/AuthorTexts.js";
import SingleText from "components/Cards/SingleText.js";
import SingleOldText from "components/Cards/SingleOldText.js";
import SingleVariantText from "components/Cards/SingleVariantText.js";

export default function Dashboard() {
  const { authorId: authorIdFromUrl } = useParams();
  const [authorId, setAuthorId] = useState(authorIdFromUrl || 1);
  const [selectedText, setSelectedText] = useState(null);
  const [firstTextId, setFirstTextId] = useState(null);  // eslint-disable-next-line
  const [author, setAuthor] = useState({});

    // update authorId when the URL parameter changes
    useEffect(() => {
      setAuthorId(authorIdFromUrl || 1);
    }, [authorIdFromUrl]);
  
    // fetch author data when authorId changes
    useEffect(() => {
      fetch(`http://localhost:8000/authors/${authorId}`)
        .then(response => response.json())
        .then(data => {
          setAuthor(data);
        })
        .catch(err => console.error(err));
    }, [authorId]);

  return (
    <>
      <div className="flex flex-wrap mt-4">
        <div className="w-full xl:w-8/12 mb-12 xl:mb-0 px-4">
          <AuthorTexts id={authorId} setSelectedText={setSelectedText} setFirstTextId={setFirstTextId} setAuthor={setAuthor} />
        </div>
        <div className="w-full xl:w-4/12 px-4">
        <SingleText textId={selectedText || firstTextId} author={author} />

        <SingleOldText textId={selectedText || firstTextId} author={author} />       
        <SingleVariantText textId={selectedText || firstTextId} author={author} />
        </div>
      </div>
    </>
  );
}
