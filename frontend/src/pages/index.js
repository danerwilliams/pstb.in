import * as React from "react"
import { majorScale, Button, TextInput, FilePicker, Dialog, Pane, Text, Autocomplete } from '../../node_modules/evergreen-ui'


const mainStyle = {
    backgroundColor: '#282a36',
    left: 0,
    top: 0,
    padding: 0,
    margin: 0,
    height: '100%',
    width: '100%',
    position: 'fixed',
};


const IndexPage = () => {
  return (
    <main style={mainStyle}>
        <Pane
        display="flex"
        alignItems="center"
        justifyContent="center"
        border="none"
        >
            <TextInput height={majorScale(6)} width={majorScale(60)} />
        </Pane>
        <Pane
        display="flex"
        alignItems="center"
        justifyContent="center"
        border="none"
        >

        </Pane>
        <Pane
        display="flex"
        alignItems="center"
        justifyContent="center"
        border="none"
        >
            <Button height={majorScale(8)} width={majorScale(24)} justifyContent="center" appearance="minimal" color="#bd93f9">
                <Text>pstb.in</Text>
            </Button>
        </Pane>
    </main>
  )
}

export default IndexPage
