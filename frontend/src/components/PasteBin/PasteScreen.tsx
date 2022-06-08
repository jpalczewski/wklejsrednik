import {Col, Container as BC, Row} from "react-bootstrap";
import React, {useEffect, useState} from "react";
import {commitMutation, useLazyLoadQuery} from "react-relay";
import {highlightPasteBinMutation} from "../../Query/SyntaxHighlight/__generated__/highlightPasteBinMutation.graphql";
import RelayEnvironment from "../../RelayEnvironment";
import {highlightPasteBin} from "../../Query/SyntaxHighlight/highlightPasteBin";
import {useNavigate, useParams} from "react-router-dom";
import {getPasteBinQuery} from "../../Query/PasteBins/__generated__/getPasteBinQuery.graphql";
import {getPasteBin} from "../../Query/PasteBins/getPasteBin";
import {Wrapper} from "../../styles/Components.style";
import {PasteReportScreen} from "./PasteReportScreen";

import {
    Accordion,
    Box,
    Button,
    Flex,
    Spacer,
    Tab,
    TabList,
    TabPanel,
    TabPanels,
    Tabs,
    Textarea,
    AccordionItem,
    AccordionPanel,
    AccordionButton,
    AccordionIcon, Img,
    HStack
} from "@chakra-ui/react";
import {ratePasteBinMutation} from "../../Query/Rating/__generated__/ratePasteBinMutation.graphql";
import {ratePasteBin} from "../../Query/Rating/ratePasteBin";
import {isPasteBinRatedMutation} from "../../Query/Rating/__generated__/isPasteBinRatedMutation.graphql";
import {isPasteBinRated} from "../../Query/Rating/isPasteBinRated";

export const PasteScreen = (props: any) => {
    const [isRated, setIsRated] = useState<boolean>(false);
    const [rate, setRate] = useState<boolean | null>(null);
    const [syntax, setSyntax] = useState<string>("");
    const pk = props.id;
    const paste = useLazyLoadQuery<getPasteBinQuery>(getPasteBin, {id: pk!});
    const [totalRating, setTotalRating] = useState(paste.activePasteBin?.edges[0]?.node?.totalRating);

    const [color, setColor] = useState("black");
    const [cursor, setCursor] = useState("crosshair");

    useEffect(() => {
        commitMutation<isPasteBinRatedMutation>(RelayEnvironment, {
            mutation: isPasteBinRated,
            variables: {paste: props.id},
            onCompleted: (response) => {
                setIsRated(response.isPasteBinRated?.isRated!);
                setRate(response.isPasteBinRated?.rate!);
            },
        });
      commitMutation<highlightPasteBinMutation>(RelayEnvironment, {
        mutation: highlightPasteBin,
        variables: { id: pk! },
        onCompleted: (response) => {
            setSyntax(response.highlightPasteBin?.highlight!)
        },
        onError: (error) => {
            setSyntax("Error")
        },
  });
  }, []);

    const navigate = useNavigate();

    const refreshRated = () => {
        commitMutation<isPasteBinRatedMutation>(RelayEnvironment, {
            mutation: isPasteBinRated,
            variables: {paste: props.id},
            onCompleted: (response) => {
                setIsRated(response.isPasteBinRated?.isRated!);
                setRate(response.isPasteBinRated?.rate!);
                setTotalRating(response.isPasteBinRated?.totalRating);
            },
        });
    };

    const ratePaste = (value: any) => {
        commitMutation<ratePasteBinMutation>(RelayEnvironment, {
            mutation: ratePasteBin,
            variables: {paste: props.id, liked: value},
            onCompleted: (response) => {
                if (response.ratePasteBin?.ok!) {
                    refreshRated()
                }
            }
        });
    }

    const handleRate = (event: any) => {
        let value = event.target.value === "like";
        if (isRated) {
            if (value === rate) {
                ratePaste(null);
            } else {
                ratePaste(value);
            }
        } else {
            ratePaste(value);
        }
    };

    return (
        <Wrapper style={{textAlign: "left"}}>
            <div className="p-3">
                <BC className="bg-white" style={{height: "75vh"}}>
                    <Row className="px-4 py-4">
                        <Flex align="center">
                            <Button colorScheme="teal" onClick={() => navigate(-1)}>Go back</Button>
                            <Spacer/>
                            {
                                isRated
                                    ?
                                    <>
                                        {
                                            rate
                                                ?

                                                <>
                                                    <Button colorScheme="blue" value="like"
                                                            onClick={handleRate}>&#128402;</Button>
                                                    <Box className="px-3">{totalRating}</Box>
                                                    <Button colorScheme="blue" variant="outline" value="dislike"
                                                            onClick={handleRate}>&#128403;</Button>
                                                </>

                                                :
                                                <>
                                                    <Button colorScheme="blue" variant="outline" value="like"
                                                            onClick={handleRate}>&#128402;</Button>
                                                    <Box className="px-3">{totalRating}</Box>
                                                    <Button colorScheme="blue" value="dislike"
                                                            onClick={handleRate}>&#128403;</Button>
                                                </>
                                        }
                                    </>
                                    :
                                    <>
                                        <Button colorScheme="blue" variant="outline" value="like"
                                                onClick={handleRate}>&#128402;</Button>
                                        <Box className="px-3">{totalRating}</Box>
                                        <Button colorScheme="blue" variant="outline" value="dislike"
                                                onClick={handleRate}>&#128403;</Button>
                                    </>
                            }
                        </Flex>
                    </Row>
                    <hr/>
                    <Row>
                        <Col md={4} className="px-5 py-3" style={{borderRight: "1px solid #eee", height: "100vh"}}>
                            <p style={{fontSize: 32}}>{paste.activePasteBin?.edges?.[0]?.node?.title}</p>
                            {paste.activePasteBin?.edges?.[0]?.node?.author !== null &&
                                <pre
                                    style={{color: color, cursor: cursor}}
                                    onClick={() => navigate(`/users/${paste.activePasteBin?.edges?.[0]?.node?.author?.id}`)}
                                    onMouseOver={() => {
                                        setColor("grey");
                                        setCursor("pointer");
                                    }}
                                    onMouseLeave={() => {
                                        setColor("black");
                                        setCursor("crosshair");
                                    }}
                                >Author: {paste.activePasteBin?.edges?.[0]?.node?.author?.username}</pre>
                            }
                            <pre>Lanuage: {paste.activePasteBin?.edges?.[0]?.node?.language}</pre>

                            <Box className="my-5">
                                <Accordion allowToggle>
                                    <AccordionItem>
                                        <h2>
                                            <AccordionButton>
                                                <Box flex='1' textAlign='left'>
                                                    Photos
                                                </Box>
                                                <AccordionIcon/>
                                            </AccordionButton>
                                        </h2>
                                        <AccordionPanel>
                                            <HStack>
                                                {paste.activePasteBin?.edges[0]?.node?.attachments.edges.map(image => {
                                                    return (
                                                        <a href={`${image?.node?.url!}`}>
                                                            <Img boxSize="100px" objectFit="cover"
                                                             src={image?.node?.url!} alt={image?.node?.url!}/>
                                                        </a>
                                                    )
                                                })}
                                            </HStack>
                                        </AccordionPanel>
                                    </AccordionItem>
                                </Accordion>
                            </Box>

                            <PasteReportScreen
                                pid={paste.activePasteBin?.edges?.[0]?.node?.id}
                                title={paste.activePasteBin?.edges?.[0]?.node?.title}/>
                        </Col>
                        <Col style={{height: "100vh"}}>
                            <Tabs className="my-5">
                                <TabList>
                                    <Tab>Code</Tab>
                                    {
                                        paste.activePasteBin?.edges?.[0]?.node?.language !== "Plain Text"
                                        &&
                                        <Tab>Highlight</Tab>
                                    }
                                </TabList>
                                <TabPanels>
                                    <TabPanel>
                                        <Textarea
                                            size="lg"
                                            rows={10}
                                            isReadOnly={true}
                                            value={paste.activePasteBin?.edges?.[0]?.node?.text}
                                        />
                                        {/*<textarea rows={10} disabled>{paste.allPasteBin?.edges?.[0]?.node?.text}</textarea>*/}
                                    </TabPanel>
                                    <TabPanel>
                                <pre className="overflow-scroll" style={{height: "80vh", width: "80vh"}}
                                     dangerouslySetInnerHTML={{__html: syntax}}></pre>
                                    </TabPanel>
                                </TabPanels>
                            </Tabs>
                        </Col>
                    </Row>
                </BC>
            </div>
        </Wrapper>
    );
}
