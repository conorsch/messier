require_relative 'spec_helper'

describe package("htop") do
  it { should be_installed }
end
