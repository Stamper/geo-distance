import React from 'react';
import { act } from 'react-dom/test-utils';
import { shallow, mount } from 'enzyme';
import Distance from '../distance';

it('renders distance component without crashing', () => {
  shallow(<Distance />);
});

describe('<Distance /> tests', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = mount( < Distance / >);
    fetch.resetMocks();
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('calculate button disabled by default', () => {
    let button = wrapper.find('.calculateButton');
    expect(button.prop('disabled')).toBeTruthy();
  });
});