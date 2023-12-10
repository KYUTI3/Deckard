import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';

export default function App() {
  return (
    <View style={styles.container}>
      <Text>Deckard</Text>
      <Text>Welcome to Deckard!</Text>
      <Button {{txt.txt1}}/>
      <Button {{txt="Sign Up"}}/>
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: '15px'
  },
  title: {
    fontWeight: 'bold';
    fontSize: 25,

  },

  normal: {
    fontWeight: 'bold',
    fontSize: '15'
  },

});
