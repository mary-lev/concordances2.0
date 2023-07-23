import React, { useState, useEffect } from "react";

export default function AuthorTexts({ id, setSelectedText, setFirstTextId }) {
  const [texts, setTexts] = useState([]);
  const [author, setAuthor] = useState({});

  useEffect(() => {
    fetch(`http://localhost:8000/texts/author/?author_id=${id}`)
      .then(response => response.json())
      .then(data => {
        setTexts(data);
        if (data.length > 0) {
          setFirstTextId(data[0].id);  // set the first text ID
        }
      })
      .catch(err => console.error(err));

    
      fetch(`http://localhost:8000/authors/${id}`)
      .then(response => response.json())
      .then(data => {
        setAuthor(data);
      })
      .catch(err => console.error(err));  // eslint-disable-next-line
  }, [id]);

  console.log(author);
  
  return (
    <>
      <div className="relative flex flex-col min-w-0 break-words bg-white w-full mb-6 shadow-lg rounded">
        <div className="rounded-t mb-0 px-4 py-3 border-0">
          <div className="flex flex-wrap items-center">
            <div className="relative w-full px-4 max-w-full flex-grow flex-1">
              <h3 className="font-semibold text-base text-blueGray-700">
                {author.name} {author.family}
              </h3>
            </div>
            <div className="relative w-full px-4 max-w-full flex-grow flex-1 text-right">
              <button
                className="bg-indigo-500 text-white active:bg-indigo-600 text-xs font-bold uppercase px-3 py-1 rounded outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150"
                type="button"
              >
                See all
              </button>
            </div>
          </div>
        </div>
        <div className="block w-full overflow-x-auto" style={{ overflowY: 'auto', maxHeight: '700px' }}>
          <table className="items-center w-full bg-transparent border-collapse">
            <thead>
              <tr>
                <th className="px-6 bg-blueGray-50 text-blueGray-500 align-middle border border-solid border-blueGray-100 py-3 text-xs uppercase border-l-0 border-r-0 whitespace-nowrap font-semibold text-left">
                  ID
                </th>
                <th className="px-6 bg-blueGray-50 text-blueGray-500 align-middle border border-solid border-blueGray-100 py-3 text-xs uppercase border-l-0 border-r-0 whitespace-nowrap font-semibold text-left">
                  Title or first string
                </th>
                <th className="px-6 bg-blueGray-50 text-blueGray-500 align-middle border border-solid border-blueGray-100 py-3 text-xs uppercase border-l-0 border-r-0 whitespace-nowrap font-semibold text-left">
                  Книга
                </th>
                <th className="px-6 bg-blueGray-50 text-blueGray-500 align-middle border border-solid border-blueGray-100 py-3 text-xs uppercase border-l-0 border-r-0 whitespace-nowrap font-semibold text-left">
                  Year
                </th>
              </tr>
            </thead>
            <tbody>
              {texts.map((text, index) => (
                <tr key={index}>
                  <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-2 text-left">
                    {text.id}
                  </td>
                  <td  className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-2 text-left" 
                  onClick={() => {
                    setSelectedText(text.id);
                }} >
                {text.title ? `${text.title} ${text.first_string}`.substring(0, 50) : text.first_string.substring(0, 50)}
                    </td>
                    <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-2">
                    {text.group_text ? `${text.group_text.title}` : '' }
                  </td>
                  <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-2">
                    {text.text_date ? `${text.text_date.year}` : ''}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}
