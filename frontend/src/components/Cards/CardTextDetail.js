import React from "react";
import { Link } from 'react-router-dom';
import CardTabs from "components/Cards/CardTabs.js";

// components

export default function CardTextDetail({text}) {
    console.log("Text", text);
  return (
    <>
      <div className="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded-lg bg-blueGray-100 border-0">
        <div className="rounded-t bg-white mb-0 px-6 py-6">
          <div className="text-center flex justify-between">
            <h6 className="text-blueGray-700 text-xl font-bold">{text && `${text.author.name} ${text.author.family}. ${text.title}`}</h6>
            <Link
  to={`/admin/dashboard/${text ? text.author_id : "#"}`}
  className="bg-lightBlue-500 text-white active:bg-lightBlue-600 font-bold uppercase text-xs px-4 py-2 rounded shadow hover:shadow-md outline-none focus:outline-none mr-1 ease-linear transition-all duration-150 inline-block"
>
  All texts
</Link>
          </div>
        </div>
        <div className="flex-auto px-4 lg:px-10 py-10 pt-0">
        <CardTabs text={text} />

        </div>
      </div>
    </>
  );
}
