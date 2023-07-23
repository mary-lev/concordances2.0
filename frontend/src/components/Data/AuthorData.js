import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

export default function AuthorData() {
  const [author, setAuthor] = useState(null);
  const { id } = useParams();

  useEffect(() => {
    fetch(`http://localhost:8000/authors/${id}`)  // replace with your FastAPI URL
      .then(response => response.json())
      .then(data => {
        setAuthor(data);
        console.log(data);
      })
      .catch(err => console.error(err));
  }, [id]);  // authorId is a dependency
  
  if (!author) {
    return 'Loading...';  // replace with a loading spinner or something similar
  }

  return (
    <>
      <div className="text-center mt-12">
          <h3 className="text-4xl font-semibold leading-normal mb-2 text-blueGray-700 mb-2">
            {author.name} {author.family}
          </h3>
          <div className="text-sm leading-normal mt-0 mb-2 text-blueGray-400 font-bold uppercase">
            <i className="fas fa-map-marker-alt mr-2 text-lg text-blueGray-400"></i>{" "}
            Los Angeles, California
          </div>
          <div className="mb-2 text-blueGray-600 mt-10">
            <i className="fas fa-briefcase mr-2 text-lg text-blueGray-400"></i>
            Solution Manager - Creative Tim Officer
          </div>
          <div className="mb-2 text-blueGray-600">
            <i className="fas fa-university mr-2 text-lg text-blueGray-400"></i>
            University of Computer Science
          </div>
      </div>
    </>
  );
}
