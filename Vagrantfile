# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.define :server do |server_config|
    # Vmware fusion box
    server_config.vm.box = "base_fusion"
    server_config.vm.box_url = "http://files.vagrantup.com/precise64_vmware_fusion.box"
    server_config.vm.synced_folder ".", "/var/lib/cfd/"
    server_config.vm.provision :shell, :path => "scripts/test-server.py"
  end

  config.vm.define :client do |client_config|
    client_config.vm.box = "base_fusion"
    client_config.vm.box_url = "http://files.vagrantup.com/precise64_vmware_fusion.box"
    client_config.vm.synced_folder ".", "/var/lib/cfd/"
    client_config.vm.provision :shell, :path => "scripts/test-client.py"
  end
end
