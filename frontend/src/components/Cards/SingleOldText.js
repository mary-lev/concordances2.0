import React, { useState, useEffect } from "react";
import SingleEmptyBlock from "./SingleEmptyBlock";

export default function SingleOldText({ textId, author }) {
  const [text, setText] = useState(null);
  console.log("Author: ", author);

  useEffect(() => {
    if (textId) {
      fetch(`http://localhost:8000/old/text/${textId}`)
        .then(response => response.json())
        .then(data => {
          setText(data);
        })
        .catch(err => console.error(err));
    }
  }, [textId]);

  // Return null if text is not loaded yet
  if (!text) return <SingleEmptyBlock text="No old orphography" />;
  if (!text.body) return <SingleEmptyBlock text="No old orphography"/>;

  return (
    <>
      <div className="relative flex flex-col min-w-0 break-words bg-white w-full mb-6 shadow-lg rounded">
        <div className="rounded-t mb-0 px-4 py-3 border-0">
          <div className="flex flex-wrap items-center">
            <div className="relative w-full px-4 max-w-full flex-grow flex-1">
              <h3 className="font-semibold text-base text-blueGray-700">
              Старая орфография
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
        <div className="block w-full overflow-x-auto">
          {/* Projects table */}
          <table className="items-center w-full bg-transparent border-collapse">
            <thead className="thead-light">
              <tr>
                <th className="px-6 bg-blueGray-50 text-blueGray-500 align-middle border border-solid border-blueGray-100 py-3 text-xs uppercase border-l-0 border-r-0 whitespace-nowrap font-semibold text-left">
                {text.title ? text.title : "* * *"}
                </th>
               
              </tr>
            </thead>
            <tbody>
              <tr>
                <th className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4 text-left">
                <div dangerouslySetInnerHTML={{ __html: text.body.replace(/\n/g, '<br/>') }} />
                <p>{text.year}</p>
                </th>
               </tr>
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}
