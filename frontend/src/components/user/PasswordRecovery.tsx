import {Button, Form, Alert} from "react-bootstrap";
import React, {useEffect, useState} from "react";
import {commitMutation} from "react-relay";
import {passwordRecoveryMutation} from "../../Query/Users/__generated__/passwordRecoveryMutation.graphql";
import relayEnvironment from "../../RelayEnvironment";
import {passwordRecovery} from "../../Query/Users/passwordRecovery";
import {useNavigate} from "react-router-dom";
import {Wrapper} from "../../styles/Components.style";

export const PasswordRecovery = () => {
    const [email, setEmail] = useState("");
    const navigate = useNavigate();
    const [error, setError] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");

    const handleSubmit = () => {
        if (email === "") return;
        commitMutation<passwordRecoveryMutation>(relayEnvironment, {
           mutation: passwordRecovery,
            variables: {email: email},
            onCompleted: response => {
               if (response.sendNewPasswordToken?.ok!) {
                   navigate("/verify", {state: {email: email, type: "recovery"}});
               }
               setError(true);
               setErrorMessage(response.sendNewPasswordToken?.response!);
            },
            onError: error => {
                setError(true);
                setErrorMessage(error.message);
            }
        });
    }

    useEffect(() => {
        const timer = setTimeout(() => {
            setError(false);
        }, 1500);
        return () => clearTimeout(timer);
    }, [error]);

    return (
        <Wrapper>
            {error &&
                <Alert variant="primary" style={{width: "50vh", margin: "auto"}}>
                    <Alert.Heading>
                        {errorMessage}
                    </Alert.Heading>
                </Alert>
            }
        <div className="Contener">

            <Form.Group className="mb-3">
                <Form.Label className="my-5">E-mail</Form.Label>
                <Form.Control
                    type="email"
                    name="email"
                    placeholder="test@test.pl"
                    value={email || ""}
                    onChange={(e) => {setEmail(e.target.value)}}
                />
        </Form.Group>
        <Button className="my-5" onClick={() => handleSubmit()}>
            Send E-Mail
        </Button>
        </div></Wrapper>
    );
}
