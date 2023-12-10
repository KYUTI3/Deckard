import { StatusBar } from 'expo-status-bar';
import Button from './components/Button';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { StyleSheet, 
  Text, 
  View 
} from 'react-native';

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <View style={styles.container}>
      <Text>Deckard</Text>
      <Text>Welcome to Deckard!</Text>
      <Button title={txt[0].txt1} />
      <Button title={txt[0].txt2}/>
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
