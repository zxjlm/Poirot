import React, { Component } from "react";
import { Container, Segment, Menu } from "semantic-ui-react";
import "semantic-ui-css/semantic.min.css";

const menuList = ["home", "font", "image", "instruction"];

export default class MenuExampleColoredInverted extends Component {
  state = { activeA: menuList[0] };

  handleAClick = (e, { name }) => this.setState({ activeA: name });

  render() {
    const { activeA } = this.state;

    return (
      <Container style={{ margin: 20 }}>
        <Segment inverted>
          <Menu inverted pointing secondary>
            {menuList.map((c) => (
              <Menu.Item
                key={c}
                name={c}
                active={activeA === c}
                onClick={this.handleAClick}
              />
            ))}
          </Menu>
        </Segment>
      </Container>
    );
  }
}
