import React, {useRef, useState, useEffect, useCallback} from "react";
import { GoogleMap, LoadScript, Marker } from '@react-google-maps/api';
import styled from 'styled-components'
import {API_URL} from "../constants";

const Clear = styled.button`
    margin: 0.25em; 
    border: none; 
    background-color: red; 
    color: white;
`

const Distance = () => {
    const apiKey = 'AIzaSyDLXmcgaErAaz8FKxWSFIdYVZEL0N3xdDM';
    const baseMapsApiUrl = `https://maps.googleapis.com/maps/api/geocode/json?key=${apiKey}&`

    const [map, setMap] = useState(null);

    const beginningInput = useRef();
    const destinationInput = useRef();

    const [currentInput, setCurrentInput] = useState(beginningInput);

    const [beginningPoint, setBeginningPoint] = useState(null);
    const [destinationPoint, setDestinationPoint] = useState(null);

    const [beginningAddress, setBeginningAddress] = useState('');
    const [destinationAddress, setDestinationAddress] = useState('');

    const [calculation, setCalculation] = useState(null);
    const [calculationError, setCalculationError] = useState('');

    const onLoad = useCallback((map) => {
        setMap(map)
    }, [])

    useEffect(() => {
        setCalculation(null);
        setCalculationError('');
    }, [beginningPoint, destinationPoint])

    const getPointSetter = () => {
        switch (currentInput) {
            case beginningInput:
                return setBeginningPoint

            case destinationInput:
                return setDestinationPoint

            default:
                return []
        }
    }

    const getAddressSetter = () => {
        switch (currentInput) {
            case beginningInput:
                return setBeginningAddress

            case destinationInput:
                return setDestinationAddress

            default:
                return []
        }
    }

    const processAddress = (value, pointSetter) => {
        fetch(`${baseMapsApiUrl}address=${value}`)
            .then(r => r.json())
            .then(r => {
                if (r.status === 'OK') {
                    currentInput.current.style.backgroundColor = 'white';
                    let result = r.results.shift();
                    let position = result.geometry.location;
                    pointSetter(position);
                    map.panTo(position);
                } else {
                    currentInput.current.style.backgroundColor = 'coral';
                    pointSetter(null);
                }
            })
            .catch((error) => {
                pointSetter(null);
                console.error(error);
                currentInput.current.style.backgroundColor = 'coral';
            });
    }

    const createPoint = (position) => {
        const point = {lat: position.lat(), lng: position.lng()};
        const pointSetter = getPointSetter();
        const addressSetter = getAddressSetter();
        currentInput.current.style.backgroundColor = 'white';
        pointSetter(point);
        fetch(`${baseMapsApiUrl}latlng=${point.lat},${point.lng}`)
            .then(r => r.json())
            .then(r => {
                if (r.status === 'OK') {
                    let result = r.results.shift();
                    addressSetter(result.formatted_address);
                }
            })
            .catch((error) => {
                console.error(error);
            });
    }

    const calculate = () => {
        const url = `${API_URL}/distance/?lat1=${beginningPoint.lat}&lng1=${beginningPoint.lng}&lat2=${destinationPoint.lat}&lng2=${destinationPoint.lng}`;
        fetch(url)
            .then(r => r.json())
            .then(r => {
                if (r.status === 'ok') {
                    setCalculation(r.data);
                }
            })
            .catch((error) => {
                setCalculationError('Calculation failed');
                console.error(error);
            });
    }

    return (
        <div style={{display: 'flex'}}>
            <div style={{flex: 1}}>
                <div style={{display: 'flex'}}>
                    <input
                        className={'inputBeginning'}
                        type={'text'}
                        ref={beginningInput}
                        style={{'margin': '0.25em'}}
                        value={beginningAddress}
                        placeholder={'Type address and press Enter'}
                        onFocus={e => setCurrentInput(beginningInput)}
                        onChange={e => setBeginningAddress(e.target.value)}
                        onKeyPress={e => {
                                if (e.key === 'Enter') {
                                    processAddress(beginningAddress, setBeginningPoint)
                                }
                            }
                        }
                    />
                    <Clear
                        className={'clearBeginning'}
                        onClick={e => {
                        beginningInput.current.style.backgroundColor = 'white';
                        setBeginningAddress('');
                        setBeginningPoint(null);
                    }}>✖</Clear>
                </div>
                <div style={{display: 'flex'}}>
                    <input
                        className={'inputDestination'}
                        type={'text'}
                        ref={destinationInput}
                        style={{'margin': '0.25em'}}
                        value={destinationAddress}
                        placeholder={'Type address and press Enter'}
                        onFocus={e => setCurrentInput(destinationInput)}
                        onChange={e => setDestinationAddress(e.target.value)}
                        onKeyPress={e => {
                                if (e.key === 'Enter') {
                                    processAddress(destinationAddress, setDestinationPoint)
                                }
                            }
                        }
                    />
                    <Clear
                        className={'clearDestination'}
                        onClick={e => {
                            destinationInput.current.style.backgroundColor = 'white';
                            setDestinationAddress('');
                            setDestinationPoint(null);
                        }}>✖</Clear>
                </div>
                <button className={'calculateButton'}
                        style={{'margin': '0.25em'}}
                        disabled={!(Boolean(beginningPoint) && Boolean(destinationPoint))}
                        onClick={calculate}>
                    Calculate
                </button>
                {calculation && <div><p>ml: {calculation.ml}</p><p>km: {calculation.km}</p></div>}
                {calculationError && <p style={{color: 'red'}}>{calculationError}</p>}
            </div>
            <LoadScript googleMapsApiKey={apiKey}>
                <GoogleMap
                    mapContainerStyle={{height: '98vh', flex: 7}}
                    center={{lat: 50.45, lng: 30.52}}
                    zoom={4}
                    onLoad={onLoad}
                    onClick={e => {
                        createPoint(e.latLng)
                    }}
                >
                    {beginningPoint && <Marker label={'A'} title={'Start point'} position={beginningPoint}/>}
                    {destinationPoint && <Marker label={'B'} title={'End point'} position={destinationPoint}/>}
                </GoogleMap>
            </LoadScript>
        </div>
    )
}

export default Distance;