import React, { useEffect, useState } from 'react';

const CardTabs = ({ text }) => {
    const [openTab, setOpenTab] = useState(1);
    const [variants, setVariants] = useState(null);
    const [old, setOldText] = useState(null);

    useEffect(() => {
        fetch(`http://localhost:8000/variant/text/${text.text_id}`)
            .then(response => response.json())
            .then(data => {
                setVariants(data);
            })
            .catch(err => console.error(err));
    }, [text.text_id]);

    useEffect(() => {
        fetch(`http://localhost:8000/old/text/${text.id}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('No old orthography available');
                }
                return response.json();
            })
            .then(data => {
                setOldText(data);
            })
            .catch(err => {
                console.error(err);
                setOldText(null);
            });
    }, [text.id]);

    console.log("Old: ", old);

    return (
        <>
            <div className="flex flex-wrap">
                <div className="w-full">
                    <ul className="flex mb-0 list-none flex-wrap pt-3 pb-4 flex-row" role="tablist">
                        <li className="-mb-px mr-2 last:mr-0 flex-auto text-center">
                            <a
                                className={
                                    "text-xs font-bold uppercase px-5 py-3 shadow-lg rounded block leading-normal " +
                                    (openTab === 1
                                        ? "text-white bg-lightBlue-600"
                                        : "text-lightBlue-600 bg-white")
                                }
                                onClick={e => {
                                    e.preventDefault();
                                    setOpenTab(1);
                                }}
                                data-toggle="tab"
                                href="#link1"
                                role="tablist"
                            >
                                Text
                            </a>
                        </li>
                        <li className="-mb-px mr-2 last:mr-0 flex-auto text-center old-text" style={{ display: (old && old.body) ? 'block' : 'none' }}>
                            <a
                                className={
                                    "text-xs font-bold uppercase px-5 py-3 shadow-lg rounded block leading-normal " +
                                    (openTab === 2
                                        ? "text-white bg-lightBlue-600"
                                        : "text-lightBlue-600 bg-white")
                                }
                                onClick={e => {
                                    e.preventDefault();
                                    setOpenTab(2);
                                }}
                                data-toggle="tab"
                                href="#link2"
                                role="tablist"
                            >
                                Old orthography
                            </a>
                        </li>


                        <li className="-mb-px mr-2 last:mr-0 flex-auto text-center">
                            <a
                                className={
                                    "text-xs font-bold uppercase px-5 py-3 shadow-lg rounded block leading-normal " +
                                    (openTab === 3
                                        ? "text-white bg-lightBlue-600"
                                        : "text-lightBlue-600 bg-white")
                                }
                                onClick={e => {
                                    e.preventDefault();
                                    setOpenTab(3);
                                }}
                                data-toggle="tab"
                                href="#link3"
                                role="tablist"
                            >
                                Publications
                            </a>
                        </li>
                        <li className="-mb-px mr-2 last:mr-0 flex-auto text-center">
                            <a
                                className={
                                    "text-xs font-bold uppercase px-5 py-3 shadow-lg rounded block leading-normal " +
                                    (openTab === 4
                                        ? "text-white bg-lightBlue-600"
                                        : "text-lightBlue-600 bg-white")
                                }
                                onClick={e => {
                                    e.preventDefault();
                                    setOpenTab(4);
                                }}
                                data-toggle="tab"
                                href="#link4"
                                role="tablist"
                            >
                                TEI
                            </a>
                        </li>
                    </ul>
                    <div className="relative flex flex-col min-w-0 break-words bg-white w-full mb-6 shadow-lg rounded">
                        <div className="px-4 py-5 flex-auto">
                            <div className="tab-content tab-space">
                                <div className={openTab === 1 ? "block" : "hidden"} id="link1">

                                    <div style={{ fontFamily: 'EB Garamond', fontSize: '18px' }} dangerouslySetInnerHTML={{ __html: text.body.replace(/\n/g, '<br/>') }} />
                                    <div style={{ fontFamily: 'EB Garamond', fontSize: '16px', paddingTop: "10px" }}><p>{text ? `Источник: ${text.source}` : ""}</p></div>

                                </div>
                                <div
                                    className={openTab === 2 ? "block" : "hidden"}
                                    id="link2"
                                >
                                    <p>
                                        {old && old.body
                                            ? <div style={{ fontFamily: 'EB Garamond', fontSize: '18px' }} dangerouslySetInnerHTML={{ __html: old.body.replace(/\n/g, '<br/>') }} />
                                            : "No old orthography available"}
                                    </p>
                                </div>

                                <div className={openTab === 3 ? "block" : "hidden"} id="link3">
                                    <p>{text.publication ? `${text.publication.author}. ${text.publication.title}. ${text.publication.city}: ${text.publication.publisher}, ${text.publication.year}` : ""}</p>
                                    {Array.isArray(variants)
                                        ? variants.map((variant, index) => (
                                            variant.publication ? (
                                                <p key={index}>
                                                    {variant.publication.title}. {variant.publication.city}: {variant.publication.publisher}, {variant.publication.year}.
                                                </p>
                                            ) : null
                                        ))
                                        : <p>No variants available</p>}
                                </div>
                                <div className={openTab === 4 ? "block" : "hidden"} id="link4">
                                    <div style={{ fontFamily: 'EB Garamond', fontSize: '14px' }}> <pre>{text.body}</pre> </div>

                                </div>





                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
};

export default CardTabs;

