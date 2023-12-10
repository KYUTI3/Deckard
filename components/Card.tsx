import React from "react"
import {
 Text, 
 Pressable, 
 StyleSheet } from "react-native"

const ClubAdvert = "Want to join a Club? Check out our list of Clubs!"

const ClubAdvert2 = "Want to add a club? Click here!"

const txt = [ 
    {txt1:"Sign Up"}, 
    {txt2: "Login"}
]

const Card = () => {
return <Text></Text>
};

const styles = StyleSheet.create({
    container: {
      flex: 1,
      padding: 24,
      backgroundColor: '#eaeaea',
    },
    title: {
      marginTop: 16,
      paddingVertical: 8,
      borderWidth: 4,
      borderColor: '#28B463',
      borderRadius: 6,
      backgroundColor: '#28B463',
      color: '#ff',
      textAlign: 'center',
      fontSize: 30,
      fontWeight: 'bold',
    },
  });
  

export default Card; 