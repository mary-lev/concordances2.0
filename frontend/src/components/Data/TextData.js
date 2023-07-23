export default function TextComponent({ text }) {
    // Helper function to construct a string from text_date properties
    const getTextDateInfo = (text_date) => {
        if (!text_date) return "";  // return empty string if text_date is null or undefined

        const monthNames = [
            "января", "февраля", "марта", "апреля", "мая", "июня",
            "июля", "августа", "сентября", "октября", "ноября", "декабря"
        ];
        const capitalizedMonthNames = [
            "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
            "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
        ];

        let info = "";
        if (text_date.day) info += `${text_date.day} `;
        if (text_date.month) {
            if (text_date.day) {
                info += `${monthNames[text_date.month - 1]} `;
            } else {
                info += `${capitalizedMonthNames[text_date.month - 1]} `;
            }
        }
        if (text_date.year) info += `${text_date.year} `;
        if (text_date.dubious_day) info += `${text_date.dubious_day} (?) `;
        if (text_date.dubious_month) info += `${text_date.dubious_month}`;
        if (text_date.dubious_year) info += `${text_date.dubious_year}(?) `;
        if (text_date.start_year && text_date.end_year) info += `(${text_date.start_year}-${text_date.end_year}) `;
        if (text_date.season) info += `${text_date.season} `;
        return info.trim();  // trim removes any trailing spaces
    };

    return (
            <div className="py-3">{getTextDateInfo(text.text_date)}</div>
    );
}
