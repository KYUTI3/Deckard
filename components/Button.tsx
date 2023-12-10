import React from "react"
import {
View, 
Text, 
Pressable,
StyleSheet,
} from "react-native"

const txt = [ 
  {txt1:"Sign Up"}, 
  {txt2: "Login"}
]

const Button = ({ onPress, title }) => (
  <View style={styles.ButtonContainer}> 
    <Pressable onPress={onPress}>
        <Text style={styles.ButtonText}>{txt}</Text>
    </Pressable>
  </View>
);

const styles = StyleSheet.create({
    screenContainer: {
      flex: 1,
      justifyContent: "center",
      padding: 16
    },
    ButtonContainer: {
      elevation: 8,
      backgroundColor: "#F39C12",
      borderRadius: 10,
      paddingVertical: 10,
      paddingHorizontal: 12,
      color: '',
    },
    ButtonText: {
      fontSize: 18,
      color: "#fff",
      fontWeight: "bold",
      alignSelf: "center",
      textTransform: "uppercase"
    }
});

export default Button;