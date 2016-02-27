# -*- mode: ruby -*-
# vi: set ft=ruby :

unless ENV.has_key?('VM_IP')
    abort('VM_IP environment variable not set')
end

Vagrant.configure(2) do |config|
  config.vm.box = "trusty64"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  config.vm.network "private_network", ip: ENV['VM_IP']

end

