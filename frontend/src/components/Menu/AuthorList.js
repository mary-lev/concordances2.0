import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const AuthorList = () => {
  const [authors, setAuthors] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/authors/') // replace with your API endpoint
      .then(response => response.json())
      .then(data => setAuthors(data))
      .catch(error => console.error('Error:', error));
  }, []);

  return (
    <ul className="md:flex-col md:min-w-full flex flex-col list-none">
      {authors.map((author) => (
        <li className="items-center" key={author.id}>
        <Link
  className={
    "text-xs uppercase py-3 font-bold block " +
    (window.location.href.indexOf(`/admin/dashboard/${author.id}`) !== -1
      ? "text-lightBlue-500 hover:text-lightBlue-600"
      : "text-blueGray-700 hover:text-blueGray-500")
  }
  to={`/admin/dashboard/${author.id}`}
>
  <i
    className={
      "fas fa-tv mr-2 text-sm " +
      (window.location.href.indexOf(`/admin/dashboard/${author.id}`) !== -1
        ? "opacity-75"
        : "text-blueGray-300")
    }
  ></i>{" "}
  {author.name} {author.family}
</Link>

        </li>
      ))}
    </ul>
  );
};

export default AuthorList;
