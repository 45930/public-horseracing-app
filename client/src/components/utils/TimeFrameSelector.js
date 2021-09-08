import React from "react";
import { Menu } from "semantic-ui-react";

class TimeFrameSelector extends React.Component {
  constructor(props) {
    super(props);
    this.state = { activeItem: "90" };
    this.onClick = this.onClick.bind(this);
  }

  onClick(e, { name }) {
    this.setState({ activeItem: name });
    this.props.onClick(e, { name });
  }

  render() {
    return (
      <Menu>
        <Menu.Item
          active={this.state.activeItem === "all_time"}
          name="all_time"
          onClick={this.onClick}
        >
          All Time
        </Menu.Item>
        <Menu.Item
          active={this.state.activeItem === "365"}
          name="365"
          onClick={this.onClick}
        >
          Last Year
        </Menu.Item>
        <Menu.Item
          active={this.state.activeItem === "90"}
          name="90"
          onClick={this.onClick}
        >
          Last 90 Days
        </Menu.Item>
        <Menu.Item
          active={this.state.activeItem === "30"}
          name="30"
          onClick={this.onClick}
        >
          Last 30 Days
        </Menu.Item>
      </Menu>
    );
  }
}

export default TimeFrameSelector;
