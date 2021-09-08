import React from "react";

const headerNameLookup = {
  track_code: "Track",
  race_date: "Date",
  race_number: "Race #",
  distance: "Distance",
  surface: "Surface",
  program_number: "Pr. Num.",
  trainer: "Trainer",
  jockey: "Jockey",
  owner: "Owner",
  horse_name: "Horse Name",
};

const decimalToFractionString = (decimal) => {
  if (decimal > 0) {
    return String(decimal).replace(".", ":");
  } else {
    return "";
  }
};

const renderedTableData = (header, pastPerformance) => {
  return (
    <td key={`td-${header}-${pastPerformance.id}`} data-label={header.name}>
      {pastPerformance[header]}
    </td>
  );
};

const renderedRunningLine = (pastPerformance) => {
  let line = [];
  ["first", "second", "third", "fourth", "fifth", "sixth"].forEach((prefix) => {
    const position = prefix + "_call_position";
    const fraction = prefix + "_fraction";
    if (!!pastPerformance[position]) {
      line.push(
        <div className="runningLineWrapper" key={prefix}>
          <div className="runningLinePosition">{pastPerformance[position]}</div>
          <div className="runningLineFraction">
            {decimalToFractionString(pastPerformance[fraction])}
          </div>
        </div>
      );
    }
  });
  return line;
};

const renderedPastPerformanceLine = (headers, pastPerformance) => {
  return (
    <tr key={`pastPerformance-${pastPerformance.id}`}>
      {headers.map((header) => {
        return renderedTableData(header, pastPerformance);
      })}
      <td data-label="Speed Figure">
        {pastPerformance.beyer_or_foreign_speed}
      </td>
      <td data-label="Running Line">{renderedRunningLine(pastPerformance)}</td>
      <td data-label="Final Position">{pastPerformance.final_call_position}</td>
      <td data-label="Final Time">
        {decimalToFractionString(pastPerformance.final_time)}
      </td>
      <td data-label="Comment">{pastPerformance.comment}</td>
    </tr>
  );
};

const PastPerformanceLines = (props) => {
  const headers = props.headers;
  const pastPerformances = props.pastPerformances.slice(0, 100);
  if (pastPerformances.length === 0) {
    return "";
  } else {
    return (
      <table className="ui basic compact unstackable table">
        <thead>
          <tr>
            {headers.map((header) => {
              return <th key={header}>{headerNameLookup[header]}</th>;
            })}
            <th>Speed Figure</th>
            <th>Running Line</th>
            <th>Final Pos.</th>
            <th>Final Time</th>
            <th>Comment</th>
          </tr>
        </thead>
        <tbody>
          {pastPerformances.map((pastPerformance) => {
            return renderedPastPerformanceLine(headers, pastPerformance);
          })}
        </tbody>
      </table>
    );
  }
};

export default PastPerformanceLines;
