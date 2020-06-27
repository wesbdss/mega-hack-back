import React, { Component } from 'react';
import { Button, Text, View,StyleSheet } from 'react-native';
import * as WebBrowser from 'expo-web-browser';
import Constants from 'expo-constants';

export default class web_browser extends Component {
  state = {
    result: null
  };

  render() {
    return (
      <View style= {styles.container}>
        <Button title="Open WebBrowser" onPress={this._handlePressButtonAsync} />
        <Text>{this.state.result && JSON.stringify(this.state.result)}</Text>
      </View>
    );
  }

  _handlePressButtonAsync = async () => {
    let result = await WebBrowser.openBrowserAsync('http://www.sbs.com.au/theboat/',{showTitle:false});
    this.setState({ result });
  };
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingTop: Constants.statusBarHeight,
    margin: 2,
    backgroundColor: '#ecf0f1',
  },
});