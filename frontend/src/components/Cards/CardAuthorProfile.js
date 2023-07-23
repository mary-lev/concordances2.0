import React, { useEffect, useState } from 'react';

export default function CardAuthorProfile({author, author_id}) {
  const [count_text, setCountText] = useState(null);
  const [count_publication, setCountPublication] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:8000/texts/count/author/?author_id=${author_id}`)
      .then(response => response.json())
      .then(data => {
        setCountText(data);
      })
      .catch(err => console.error(err));
  }, [author_id]);

  useEffect(() => {
    fetch(`http://localhost:8000/publications/count/${author_id}`)
      .then(response => response.json())
      .then(data => {
        setCountPublication(data);
      })
      .catch(err => console.error(err));
  }, [author_id]);

  return (
    <>
      <div className="relative flex flex-col min-w-0 break-words bg-white w-full mb-6 shadow-xl rounded-lg mt-16">
        <div className="px-6">
          <div className="flex flex-wrap justify-center">
            <div className="w-full px-4 flex justify-center">
              <div className="relative">
              <img alt="..." src={require(`assets/img/${author_id}.jpg`)}
      className="shadow-xl rounded-full h-auto align-middle border-none absolute -m-16 -ml-20 lg:-ml-16 max-w-150-px"
    />
              </div>
            </div>
            <div className="w-full px-4 text-center mt-20">
  <div className="flex justify-center py-4 lg:pt-4 pt-8">
    <div className="flex-1 p-3 text-center">
      <span className="text-xl font-bold block uppercase tracking-wide text-blueGray-600">
        {count_text}
      </span>
      <span className="text-sm text-blueGray-400">Texts</span>
    </div>
    <div className="flex-1 p-3 text-center">
      <span className="text-xl font-bold block uppercase tracking-wide text-blueGray-600">
        {count_publication}
      </span>
      <span className="text-sm text-blueGray-400">Publications</span>
    </div>
    <div className="flex-1 p-3 text-center">
      <span className="text-xl font-bold block uppercase tracking-wide text-blueGray-600">
        89
      </span>
      <span className="text-sm text-blueGray-400">Comments</span>
    </div>
  </div>
</div>

          </div>
          <div className="text-center mt-12">
            <h3 className="text-xl font-semibold leading-normal mb-2 text-blueGray-700 mb-2">
            {`${author.name} ${author.family}`}
            </h3>
            <div className="mb-2 text-blueGray-600">
              <i className="fas fa-map-marker-alt mr-2 text-lg text-blueGray-400"></i>{" "}
              {`${author.birth_location} ${author.year_birth}`}
            </div>
            <div className="mb-2 text-blueGray-600">
              <i className="fas fa-university mr-2 text-lg text-blueGray-400"></i>
              {`${author.death_location} ${author.year_death}`}
            </div>
          </div>
          <div className="mt-10 py-10 border-t border-blueGray-200 text-center">
            <div className="flex flex-wrap justify-center">
              <div className="w-full lg:w-9/12 px-4">
                <p className="mb-4 text-lg leading-relaxed text-blueGray-700">
                  An artist of considerable range, Jenna the name taken by
                  Melbourne-raised, Brooklyn-based Nick Murphy writes, performs
                  and records all of his own music, giving it a warm, intimate
                  feel with a solid groove structure. An artist of considerable
                  range.
                </p>
                <a
                  href="#pablo"
                  className="font-normal text-lightBlue-500"
                  onClick={(e) => e.preventDefault()}
                >
                  Show more
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
