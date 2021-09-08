import React from "react";
import { Link } from "react-router-dom";

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

const linkToGenerator = (header, result) => {
  switch (header) {
    case "trainer":
      return `/trainers/${result.trainer_id}`;
    case "jockey":
      return `/jockeys/${result.jockey_id}`;
    case "owner":
      return `/owners/${result.owner_id}`;
    case "horse_name":
      return `/horses/${result.horse_id}`;
    case "track_code":
      return `/tracks/${result.track_code}`;
    case "race_number":
      return `/races/${result.race_id}`;
  }
};

const calculateKey = (result) => {
  const { horse_id, race_id, horse_name } = result;
  return `${horse_id}-${race_id}-${horse_name}`;
};

const calculateClass = (header, value) => {
  if (header === "program_number") {
    switch (value) {
      case "1":
      case "1a":
      case "1x":
        return "program-number-one";
      case "2":
      case "2b":
        return "program-number-two";
      case "3":
        return "program-number-three";
      case "4":
        return "program-number-four";
      case "5":
        return "program-number-five";
      case "6":
        return "program-number-six";
      case "7":
        return "program-number-seven";
      case "8":
        return "program-number-eight";
      case "9":
        return "program-number-nine";
      case "10":
        return "program-number-ten";
      case "11":
        return "program-number-eleven";
      case "12":
        return "program-number-twelve";
      default:
        return "program-number";
    }
  }
};

const renderedTableData = (header, result) => {
  const linkTo = linkToGenerator(header, result);
  if (!!linkTo) {
    return (
      <td
        key={`td-${header}-${calculateKey(result)}`}
        data-label={headerNameLookup[header]}
        className="cell-highlight"
      >
        <Link className="rowLink" to={linkTo}>
          {result[header]}
        </Link>
      </td>
    );
  } else {
    return (
      <td
        key={`td-${header}-${calculateKey(result)}`}
        data-label={header.name}
        className={calculateClass(header, result[header])}
      >
        {result[header]}
      </td>
    );
  }
};

const renderedResultLine = (headers, result, complete = true) => {
  if (complete) {
    return (
      <tr key={`result-${calculateKey(result)}`}>
        {headers.map((header) => {
          return renderedTableData(header, result);
        })}
        <td data-label="Final Position">{result.final_position}</td>
        <td data-label="Final Odds">{result.odds}</td>
      </tr>
    );
  } else {
    if (result.scratched) {
      return (
        <tr key={`result-${calculateKey(result)}`}>
          {headers.map((header) => {
            return renderedTableData(header, result);
          })}
          <td data-label="Morning Line Odds">{result.morning_line_odds}</td>
          <td data-label="Win Prob" style={{ textDecoration: "line-through" }}>
            {result.predicted_win_probability}
          </td>
          <td
            data-label="Expected Perf"
            style={{ textDecoration: "line-through" }}
          >
            {result.predicted_individual_perf}
          </td>
          <td data-label="Scratched">{"SCR"}</td>
        </tr>
      );
    } else {
      return (
        <tr key={`result-${calculateKey(result)}`}>
          {headers.map((header) => {
            return renderedTableData(header, result);
          })}
          <td data-label="Morning Line Odds">{result.morning_line_odds}</td>
          <td data-label="Win Prob">{result.predicted_win_probability}</td>
          <td data-label="Expected Perf">{result.predicted_individual_perf}</td>
          <td data-label="Scratched"></td>
        </tr>
      );
    }
  }
};

const decimalToFractionString = (decimal) => {
  if (decimal > 0) {
    return String(decimal).replace(".", ":");
  } else {
    return "";
  }
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

const renderedPastPerformances = (pastPerformances) => {
  if (pastPerformances.length > 0) {
    return (
      <table className="ui basic compact unstackable table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Track</th>
            <th>Surface</th>
            <th>Speed</th>
            <th>Purse</th>
            <th>Running Line</th>
            <th>Finish</th>
          </tr>
        </thead>
        <tbody>
          {pastPerformances.map((pp) => {
            return (
              <tr>
              <td data-label="Date">{pp.race_date}</td>
              <td data-label="Track">{pp.track_code}</td>
              <td data-label="Surface">{pp.surface}</td>
              <td data-label="Speed">{pp.beyer_or_foreign_speed}</td>
              <td data-label="Purse">{pp.purse}k</td>
              <td data-label="Running Line">{renderedRunningLine(pp)}</td>
              <td data-label="Finish">{pp.final_call_position}</td>
              </tr>
            )})
          }
          </tbody>
          </table>
    )
  }
}

const renderedEntrant = (result, pps, liveOdds, liveOddsUpdate) => {
  let textDecoration = '';
  if (result.scratched) {
    textDecoration = 'line-through'
  }
  return (
    <div className="ui middle aligned grid item" key={result.id}>
      <div className="twelve wide column">
        <div className="ui grid">
          <div className="row">
            <div className={`one wide column ${calculateClass('program_number', result.program_number)}`}>
              {result.program_number}
            </div>
            <div className="three wide column">
            <Link className="rowLink" to={linkToGenerator('horse_name', result)}>
              <h3 className="ui container" style={{textDecoration: textDecoration}}>{result.horse_name}</h3>
            </Link>
            </div>
            <div className="two wide column">
              <div className="ui text container" style={{textDecoration: textDecoration}}>M-L: {result.morning_line_odds}</div>
            </div>
            <div className="five wide column">
              <div className="ui text container">Live Odds: <input
                  type="text"
                  value={liveOdds}
                  onChange={liveOddsUpdate.bind(this, result.id)}
                />
              </div>
            </div>
            <div className="two wide column">
              <div className="ui text container" style={{textDecoration: textDecoration}}>Pred: {result.predicted_win_probability}</div>
            </div>
          </div>
          <div className="row">
            {renderedPastPerformances(pps)}
          </div>
        </div>
        {/* <div className="row"></div>
        <div className="row"></div>
        <div className="row"></div> */}
      </div>
      <div className="four wide column">
        <div className="row segment">Age: {result.age}</div>
        <div className="row segment">Sex: {result.sex}</div>
        <div className="row segment">Sire: {result.sire}</div>
        <div className="row segment">
          Jockey: <Link className="rowLink" to={linkToGenerator('jockey', result)}>
            {result.jockey}
          </Link>
        </div>
        <div className="row segment">
          Trainer: <Link className="rowLink" to={linkToGenerator('trainer', result)}>
            {result.trainer}
          </Link>
        </div>
        <div className="row segment">
          Owner: <Link className="rowLink" to={linkToGenerator('owner', result)}>
            {result.owner}
          </Link>
        </div>
      </div>
    </div>
  )
};

const ResultLines = (props) => {
  const headers = props.headers;
  const results = props.results.slice(0, 100);
  const pastPerformances = props.pastPerformances || {};
  const liveOdds = props.liveOdds || {};
  const liveOddsUpdate = props.liveOddsUpdate || function() { return ''; };
  if (results.length === 0) {
    return "";
  } else if (results.every((r) => r.final_position === null)) {
    return (
      <div className="ui divided items">
        {results.map((result) => {
          let pps;
          let liveOddEntrant;
          if(result.id in pastPerformances) {
            pps = pastPerformances[result.id]
          } else {
            pps = []
          }
          if(result.id in liveOdds) {
            liveOddEntrant = liveOdds[result.id]
          } else {
            liveOddEntrant = ''
          }
          return renderedEntrant(result, pps, liveOddEntrant, liveOddsUpdate);
        })}
      </div>
    );
  } else {
    return (
      <table className="ui basic compact unstackable table">
        <thead>
          <tr>
            {headers.map((header) => {
              return <th key={header}>{headerNameLookup[header]}</th>;
            })}
            <th>Final Pos.</th>
            <th>Final Odds</th>
          </tr>
        </thead>
        <tbody>
          {results.map((result) => {
            return renderedResultLine(headers, result);
          })}
        </tbody>
      </table>
    );
  }
};

ResultLines.defaultProps = {
  headers: [],
  results: [],
};

// Pass an array of headers and an array of results
// functional component will render a table with those headers, and those results
// last columns will always be result-specific data
export default ResultLines;
