# -*- mode: ruby -*-
# vi: set ft=ruby :


Vagrant.configure(2) do |config|


  # Shared VirtualBox settings for all hosts.
  config.vm.box = "fgrehm/trusty64-lxc"
  config.vm.box = "ubuntu/trusty64"

  config.vm.box_check_update = false
  config.vm.network "private_network", type: "dhcp"
  config.vm.synced_folder ".", "/vagrant", disabled: true

  config.vm.provider :virtualbox do |v|
    v.memory = 256
  end

  config.vm.define "server" do |server|
    server.vm.hostname = "server"
  end

  config.vm.define "client" do |client|
    client.vm.hostname = "client"
    client.vm.provision :ansible do |ansible|
      ansible.playbook = "test/default.yml"
      ansible.limit = "all"
      # ansible_spec expects groups, so we'll make redundant groups.
      ansible.groups = {
        "server" => "server",
        "client" => "client",
      }
    end
  end
  # config.vm.provision "shell", inline: <<-SHELL
  #   sudo apt-get update
  #   sudo apt-get install -y apache2
  # SHELL
end
