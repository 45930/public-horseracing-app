import React from "react";
import { Link } from "react-router-dom";

const renderedFeatureName = (title, row) => {
  switch (title) {
    case "Jockey":
      return (
        <td key={row.id} className="cell-highlight">
          <Link className="rowLink" to={`/jockeys/${row.id}`}>
            {row.feature_name}
          </Link>
        </td>
      );
    case "Trainer":
      return (
        <td key={row.id} className="cell-highlight">
          <Link className="rowLink" to={`/trainers/${row.id}`}>
            {row.feature_name}
          </Link>
        </td>
      );
    case "Owner":
      return (
        <td key={row.id} className="cell-highlight">
          <Link className="rowLink" to={`/owners/${row.id}`}>
            {row.feature_name}
          </Link>
        </td>
      );
    default:
      return <td>{row.feature_name}</td>;
  }
};

const StatisticTable = (props) => {
  const title = props.title;
  const data = props.data;
  if (data.length === 0) {
    return "";
  } else {
    return (
      <table className="ui basic compact unstackable table">
        <thead>
          <tr className="ui center aligned">
            <th colSpan="3">{title} Win %</th>
          </tr>
        </thead>
        <thead>
          <tr>
            <th>{title}</th>
            <th>Starts</th>
            <th>Wins</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row) => {
            return (
              <tr key={row.feature_name}>
                {renderedFeatureName(title, row)}
                <td>{row.starts}</td>
                <td>
                  {row.wins + 0} ({Math.round((row.wins * 100) / row.starts, 2)}
                  %)
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    );
  }
};

StatisticTable.defaultProps = {
  title: "",
  data: [],
};

// Pass an string title and an array of data
// functional component will render a table with that title and that data
export default StatisticTable;
